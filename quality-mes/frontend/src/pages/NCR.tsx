import { useEffect, useState } from 'react'
import {
  Table, Button, Modal, Form, Input, Space, message, Popconfirm, Card, Tabs,
  Select, DatePicker, Tag, Descriptions, Empty, Row, Col, Divider
} from 'antd'
import { PlusOutlined, EyeOutlined, DeleteOutlined } from '@ant-design/icons'
import api from '../services/api'
import dayjs from 'dayjs'

interface CAPA {
  id: number; capa_no: string; ncr_id: number; type: string; title: string
  description: string; root_cause: string | null; action_plan: string | null
  assigned_to: number | null; status: string; due_date: string | null
  completed_date: string | null; verified_by: number | null; effectiveness: string | null
  assignee: any; verifier: any; created_at: string
}

interface NCR {
  id: number; ncr_no: string; title: string; description: string; severity: string
  source_type: string | null; source_id: number | null; reported_by: number
  assigned_to: number | null; status: string; due_date: string | null
  resolution: string | null; reporter: any; assignee: any; capas: CAPA[]
  created_at: string; updated_at: string
}

export default function NCRPage() {
  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Bao cao su khong phu hop (NCR) va Khac phuc (CAPA)</h2>
      <Tabs
        items={[
          { key: 'ncrs', label: 'NCR - Su khong phu hop', children: <NCRTab /> },
          { key: 'capas', label: 'CAPA - Hanh dong khac phuc', children: <CAPATab /> },
        ]}
      />
    </div>
  )
}

const severityColors: Record<string, string> = { critical: 'red', major: 'orange', minor: 'blue' }
const severityLabels: Record<string, string> = { critical: 'Nghiem trong', major: 'Lon', minor: 'Nho' }
const ncrStatusColors: Record<string, string> = { open: 'red', investigating: 'orange', resolved: 'blue', closed: 'green' }
const ncrStatusLabels: Record<string, string> = { open: 'Mo', investigating: 'Dang dieu tra', resolved: 'Da xu ly', closed: 'Dong' }
const capaStatusColors: Record<string, string> = { open: 'red', in_progress: 'orange', completed: 'blue', verified: 'green' }
const capaStatusLabels: Record<string, string> = { open: 'Mo', in_progress: 'Dang thuc hien', completed: 'Hoan thanh', verified: 'Da xac nhan' }

function NCRTab() {
  const [ncrs, setNcrs] = useState<NCR[]>([])
  const [loading, setLoading] = useState(false)
  const [createOpen, setCreateOpen] = useState(false)
  const [detailOpen, setDetailOpen] = useState(false)
  const [selected, setSelected] = useState<NCR | null>(null)
  const [capaOpen, setCapaOpen] = useState(false)
  const [statusFilter, setStatusFilter] = useState<string | undefined>()
  const [form] = Form.useForm()
  const [capaForm] = Form.useForm()
  const [users, setUsers] = useState<{ id: number; full_name: string }[]>([])

  const fetchData = async () => {
    setLoading(true)
    try {
      const params: any = {}
      if (statusFilter) params.status = statusFilter
      const [res, uRes] = await Promise.all([api.get('/ncr/', { params }), api.get('/users/lookup')])
      setNcrs(res.data); setUsers(uRes.data)
    } catch { message.error('Loi tai du lieu') }
    finally { setLoading(false) }
  }

  useEffect(() => { fetchData() }, [statusFilter])

  const handleCreate = async (values: any) => {
    try {
      await api.post('/ncr/', { ...values, due_date: values.due_date?.toISOString() })
      message.success('Tao NCR thanh cong')
      setCreateOpen(false); form.resetFields(); fetchData()
    } catch (err: any) { message.error(err.response?.data?.detail || 'Loi') }
  }

  const handleStatusChange = async (id: number, status: string) => {
    await api.put(`/ncr/${id}/status`, null, { params: { status } })
    message.success('Cap nhat trang thai thanh cong')
    fetchData()
  }

  const handleDelete = async (id: number) => {
    await api.delete(`/ncr/${id}`)
    message.success('Xoa NCR thanh cong')
    fetchData()
  }

  const handleCreateCAPA = async (values: any) => {
    if (!selected) return
    try {
      await api.post(`/ncr/${selected.id}/capas`, {
        ...values,
        due_date: values.due_date?.toISOString(),
        completed_date: values.completed_date?.toISOString(),
      })
      message.success('Tao CAPA thanh cong')
      setCapaOpen(false); capaForm.resetFields(); fetchData()
    } catch (err: any) { message.error(err.response?.data?.detail || 'Loi') }
  }

  const handleUpdateCAPAStatus = async (capaId: number, status: string) => {
    await api.put(`/ncr/capas/${capaId}/status`, null, { params: { status } })
    message.success('Cap nhat CAPA thanh cong')
    fetchData()
  }

  const columns = [
    { title: 'So NCR', dataIndex: 'ncr_no', key: 'no', width: 110 },
    { title: 'Tieu de', dataIndex: 'title', key: 'title', ellipsis: true },
    { title: 'Muc do', key: 'severity', width: 100, render: (_: any, r: NCR) => <Tag color={severityColors[r.severity]}>{severityLabels[r.severity]}</Tag> },
    { title: 'Nguon', key: 'source', width: 80, render: (_: any, r: NCR) => r.source_type?.toUpperCase() || '-' },
    { title: 'Nguoi bao', key: 'reporter', width: 120, render: (_: any, r: NCR) => r.reporter?.full_name },
    { title: 'Trang thai', key: 'status', width: 120, render: (_: any, r: NCR) => <Tag color={ncrStatusColors[r.status]}>{ncrStatusLabels[r.status]}</Tag> },
    { title: 'Han', key: 'due', width: 100, render: (_: any, r: NCR) => r.due_date ? dayjs(r.due_date).format('DD/MM/YYYY') : '-' },
    {
      title: 'Thao tac', key: 'actions', width: 250,
      render: (_: any, r: NCR) => (
        <Space>
          <Button size="small" icon={<EyeOutlined />} onClick={() => { setSelected(r); setDetailOpen(true) }}>Chi tiet</Button>
          {r.status === 'open' && (
            <Button size="small" onClick={() => handleStatusChange(r.id, 'investigating')}>Dieu tra</Button>
          )}
          {r.status === 'investigating' && (
            <Button size="small" type="primary" onClick={() => handleStatusChange(r.id, 'resolved')}>Da xu ly</Button>
          )}
          {r.status === 'resolved' && (
            <Button size="small" onClick={() => handleStatusChange(r.id, 'closed')}>Dong</Button>
          )}
          <Popconfirm title="Xoa NCR nay?" onConfirm={() => handleDelete(r.id)}>
            <Button size="small" danger icon={<DeleteOutlined />} />
          </Popconfirm>
        </Space>
      ),
    },
  ]

  return (
    <Card>
      <div className="flex justify-between mb-4">
        <Select
          allowClear placeholder="Loc trang thai" style={{ width: 180 }}
          value={statusFilter} onChange={setStatusFilter}
          options={Object.entries(ncrStatusLabels).map(([k, v]) => ({ label: v, value: k }))}
        />
        <Button type="primary" icon={<PlusOutlined />} onClick={() => { form.resetFields(); setCreateOpen(true) }}>
          Tao NCR moi
        </Button>
      </div>
      <Table dataSource={ncrs} columns={columns} rowKey="id" loading={loading} size="middle" />

      <Modal title="Tao NCR moi" open={createOpen} onCancel={() => setCreateOpen(false)} footer={null} width={600}>
        <Form form={form} layout="vertical" onFinish={handleCreate}>
          <Form.Item name="ncr_no" label="So NCR" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="title" label="Tieu de" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="description" label="Mo ta chi tiet" rules={[{ required: true }]}><Input.TextArea rows={4} /></Form.Item>
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="severity" label="Muc do" initialValue="minor">
                <Select options={Object.entries(severityLabels).map(([k, v]) => ({ label: v, value: k }))} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="source_type" label="Nguon phat hien">
                <Select allowClear options={[
                  { label: 'IQC - Dau vao', value: 'iqc' },
                  { label: 'IPQC - Qua trinh', value: 'ipqc' },
                  { label: 'OQC - Thanh pham', value: 'oqc' },
                  { label: 'Khac', value: 'other' },
                ]} />
              </Form.Item>
            </Col>
          </Row>
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="reported_by" label="Nguoi bao cao" rules={[{ required: true }]}>
                <Select showSearch optionFilterProp="label" placeholder="Chon nguoi bao cao" options={users.map(u => ({ label: u.full_name, value: u.id }))} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="assigned_to" label="Nguoi xu ly">
                <Select allowClear showSearch optionFilterProp="label" placeholder="Chon nguoi xu ly" options={users.map(u => ({ label: u.full_name, value: u.id }))} />
              </Form.Item>
            </Col>
          </Row>
          <Form.Item name="due_date" label="Han xu ly"><DatePicker className="w-full" /></Form.Item>
          <Button type="primary" htmlType="submit" block>Tao NCR</Button>
        </Form>
      </Modal>

      <Modal title="Chi tiet NCR" open={detailOpen} onCancel={() => setDetailOpen(false)} footer={null} width={800}>
        {selected && (
          <div>
            <Descriptions column={2} bordered size="small" className="mb-4">
              <Descriptions.Item label="So NCR">{selected.ncr_no}</Descriptions.Item>
              <Descriptions.Item label="Trang thai"><Tag color={ncrStatusColors[selected.status]}>{ncrStatusLabels[selected.status]}</Tag></Descriptions.Item>
              <Descriptions.Item label="Muc do"><Tag color={severityColors[selected.severity]}>{severityLabels[selected.severity]}</Tag></Descriptions.Item>
              <Descriptions.Item label="Nguon">{selected.source_type?.toUpperCase() || 'Khac'}</Descriptions.Item>
              <Descriptions.Item label="Nguoi bao">{selected.reporter?.full_name}</Descriptions.Item>
              <Descriptions.Item label="Nguoi xu ly">{selected.assignee?.full_name || 'Chua phan cong'}</Descriptions.Item>
              <Descriptions.Item label="Han xu ly">{selected.due_date ? dayjs(selected.due_date).format('DD/MM/YYYY') : '-'}</Descriptions.Item>
              <Descriptions.Item label="Ngay tao">{dayjs(selected.created_at).format('DD/MM/YYYY HH:mm')}</Descriptions.Item>
            </Descriptions>
            <h4 className="font-bold mb-1">Mo ta:</h4>
            <p className="mb-4 whitespace-pre-wrap bg-gray-50 p-3 rounded">{selected.description}</p>
            {selected.resolution && (
              <>
                <h4 className="font-bold mb-1">Giai phap:</h4>
                <p className="mb-4 whitespace-pre-wrap bg-green-50 p-3 rounded">{selected.resolution}</p>
              </>
            )}
            <Divider />
            <div className="flex justify-between items-center mb-2">
              <h4 className="font-bold">CAPA - Hanh dong khac phuc ({selected.capas.length})</h4>
              <Button type="primary" size="small" icon={<PlusOutlined />} onClick={() => { capaForm.resetFields(); setCapaOpen(true) }}>
                Them CAPA
              </Button>
            </div>
            {selected.capas.length === 0 ? (
              <Empty description="Chua co CAPA" />
            ) : (
              selected.capas.map((capa) => (
                <Card key={capa.id} size="small" className="mb-2" title={`${capa.capa_no} - ${capa.title}`}
                  extra={<Tag color={capaStatusColors[capa.status]}>{capaStatusLabels[capa.status]}</Tag>}>
                  <Descriptions size="small" column={3}>
                    <Descriptions.Item label="Loai">{capa.type === 'corrective' ? 'Khac phuc' : 'Phong ngua'}</Descriptions.Item>
                    <Descriptions.Item label="Nguoi phu trach">{capa.assignee?.full_name || '-'}</Descriptions.Item>
                    <Descriptions.Item label="Han">{capa.due_date ? dayjs(capa.due_date).format('DD/MM/YYYY') : '-'}</Descriptions.Item>
                  </Descriptions>
                  {capa.root_cause && <p className="text-sm"><strong>Nguyen nhan goc:</strong> {capa.root_cause}</p>}
                  {capa.action_plan && <p className="text-sm"><strong>Ke hoach:</strong> {capa.action_plan}</p>}
                  {capa.effectiveness && <p className="text-sm"><strong>Hieu qua:</strong> {capa.effectiveness}</p>}
                  <Space className="mt-2">
                    {capa.status === 'open' && <Button size="small" onClick={() => handleUpdateCAPAStatus(capa.id, 'in_progress')}>Bat dau</Button>}
                    {capa.status === 'in_progress' && <Button size="small" type="primary" onClick={() => handleUpdateCAPAStatus(capa.id, 'completed')}>Hoan thanh</Button>}
                    {capa.status === 'completed' && <Button size="small" onClick={() => handleUpdateCAPAStatus(capa.id, 'verified')}>Xac nhan</Button>}
                  </Space>
                </Card>
              ))
            )}
          </div>
        )}
      </Modal>

      <Modal title="Them CAPA" open={capaOpen} onCancel={() => setCapaOpen(false)} footer={null} width={600}>
        <Form form={capaForm} layout="vertical" onFinish={handleCreateCAPA}>
          <Form.Item name="capa_no" label="So CAPA" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="title" label="Tieu de" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="type" label="Loai" initialValue="corrective">
            <Select options={[{ label: 'Khac phuc', value: 'corrective' }, { label: 'Phong ngua', value: 'preventive' }]} />
          </Form.Item>
          <Form.Item name="description" label="Mo ta" rules={[{ required: true }]}><Input.TextArea rows={2} /></Form.Item>
          <Form.Item name="root_cause" label="Nguyen nhan goc"><Input.TextArea rows={2} /></Form.Item>
          <Form.Item name="action_plan" label="Ke hoach hanh dong"><Input.TextArea rows={2} /></Form.Item>
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="assigned_to" label="Nguoi phu trach">
                <Select allowClear showSearch optionFilterProp="label" placeholder="Chon nguoi phu trach" options={users.map(u => ({ label: u.full_name, value: u.id }))} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="due_date" label="Han hoan thanh"><DatePicker className="w-full" /></Form.Item>
            </Col>
          </Row>
          <Button type="primary" htmlType="submit" block>Them CAPA</Button>
        </Form>
      </Modal>
    </Card>
  )
}

function CAPATab() {
  const [ncrs, setNcrs] = useState<NCR[]>([])
  const [loading, setLoading] = useState(false)
  const [statusFilter, setStatusFilter] = useState<string | undefined>()

  const fetchData = async () => {
    setLoading(true)
    try {
      const res = await api.get('/ncr/')
      setNcrs(res.data)
    } catch { message.error('Loi tai du lieu') }
    finally { setLoading(false) }
  }

  useEffect(() => { fetchData() }, [])

  const allCapas = ncrs.flatMap(ncr => ncr.capas.map(capa => ({ ...capa, ncr_no: ncr.ncr_no, ncr_title: ncr.title, ncr_severity: ncr.severity })))
  const filtered = statusFilter ? allCapas.filter(c => c.status === statusFilter) : allCapas

  return (
    <Card>
      <div className="flex justify-between mb-4">
        <Select
          allowClear placeholder="Loc trang thai" style={{ width: 180 }}
          value={statusFilter} onChange={setStatusFilter}
          options={Object.entries(capaStatusLabels).map(([k, v]) => ({ label: v, value: k }))}
        />
      </div>
      <Table
        dataSource={filtered}
        rowKey="id"
        loading={loading}
        size="middle"
        columns={[
          { title: 'So CAPA', dataIndex: 'capa_no', key: 'no', width: 110 },
          { title: 'Tieu de', dataIndex: 'title', key: 'title', ellipsis: true },
          { title: 'Loai', key: 'type', width: 100, render: (_: any, r: any) => r.type === 'corrective' ? 'Khac phuc' : 'Phong ngua' },
          { title: 'NCR', key: 'ncr', width: 120, render: (_: any, r: any) => <a>{r.ncr_no}</a> },
          { title: 'Nguoi phu trach', key: 'assignee', width: 130, render: (_: any, r: any) => r.assignee?.full_name || '-' },
          { title: 'Trang thai', key: 'status', width: 130, render: (_: any, r: any) => <Tag color={capaStatusColors[r.status]}>{capaStatusLabels[r.status]}</Tag> },
          { title: 'Han', key: 'due', width: 100, render: (_: any, r: any) => r.due_date ? dayjs(r.due_date).format('DD/MM/YYYY') : '-' },
          { title: 'Hieu qua', key: 'eff', width: 100, render: (_: any, r: any) => r.effectiveness || '-' },
        ]}
      />
    </Card>
  )
}
