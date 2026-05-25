import { useEffect, useState } from 'react'
import {
  Table, Button, Modal, Form, Input, Space, message, Popconfirm, Tabs, Card,
  Select, InputNumber, DatePicker, Tag, Descriptions, Upload,
} from 'antd'
import { PlusOutlined, SearchOutlined, DeleteOutlined, EditOutlined, EyeOutlined, DownloadOutlined, UploadOutlined } from '@ant-design/icons'
import api from '../services/api'
import AQLHelper from '../components/AQLHelper'
import dayjs from 'dayjs'

interface Supplier {
  id: number; code: string; name: string; contact_person: string | null
  phone: string | null; email: string | null; address: string | null; status: string
}

interface Material {
  id: number; code: string; name: string; specification: string | null
  unit: string; supplier_id: number; supplier: Supplier | null
}

interface IQCResult {
  id: number; item_name: string; specification: string | null
  measured_value: number; standard_min: number | null; standard_max: number | null
  result: string; notes: string | null
}

interface IQCInspection {
  id: number; inspection_no: string; material_id: number; supplier_id: number
  lot_no: string; quantity: number; sample_size: number; inspection_date: string
  inspector_id: number; status: string; notes: string | null
  material: Material | null; supplier: Supplier | null; inspector: any
  results: IQCResult[]
}

export default function IQCPage() {
  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Kiem tra chat luong dau vao (IQC)</h2>
      <Tabs
        items={[
          { key: 'inspections', label: 'Phieu kiem tra', children: <InspectionTab /> },
          { key: 'suppliers', label: 'Nha cung cap', children: <SupplierTab /> },
          { key: 'materials', label: 'Nguyen vat lieu', children: <MaterialTab /> },
        ]}
      />
    </div>
  )
}

function SupplierTab() {
  const [suppliers, setSuppliers] = useState<Supplier[]>([])
  const [loading, setLoading] = useState(false)
  const [modalOpen, setModalOpen] = useState(false)
  const [editing, setEditing] = useState<Supplier | null>(null)
  const [form] = Form.useForm()
  const [search, setSearch] = useState('')

  const fetchSuppliers = async () => {
    setLoading(true)
    try {
      const res = await api.get('/iqc/suppliers', { params: { search } })
      setSuppliers(res.data)
    } catch { message.error('Loi tai danh sach nha cung cap') }
    finally { setLoading(false) }
  }

  useEffect(() => { fetchSuppliers() }, [search])

  const handleSave = async (values: any) => {
    try {
      if (editing) {
        await api.put(`/iqc/suppliers/${editing.id}`, values)
        message.success('Cap nhat nha cung cap thanh cong')
      } else {
        await api.post('/iqc/suppliers', values)
        message.success('Them nha cung cap thanh cong')
      }
      setModalOpen(false); form.resetFields(); setEditing(null); fetchSuppliers()
    } catch (err: any) { message.error(err.response?.data?.detail || 'Loi') }
  }

  const handleDelete = async (id: number) => {
    await api.delete(`/iqc/suppliers/${id}`)
    message.success('Xoa nha cung cap thanh cong')
    fetchSuppliers()
  }

  const openEdit = (record: Supplier) => {
    setEditing(record); form.setFieldsValue(record); setModalOpen(true)
  }

  const columns = [
    { title: 'Ma NCC', dataIndex: 'code', key: 'code', width: 100 },
    { title: 'Ten nha cung cap', dataIndex: 'name', key: 'name' },
    { title: 'Nguoi lien he', dataIndex: 'contact_person', key: 'contact_person' },
    { title: 'SDT', dataIndex: 'phone', key: 'phone', width: 120 },
    { title: 'Email', dataIndex: 'email', key: 'email' },
    {
      title: 'Thao tac', key: 'actions', width: 150,
      render: (_: any, record: Supplier) => (
        <Space>
          <Button size="small" icon={<EditOutlined />} onClick={() => openEdit(record)} />
          <Popconfirm title="Xoa nha cung cap nay?" onConfirm={() => handleDelete(record.id)}>
            <Button size="small" danger icon={<DeleteOutlined />} />
          </Popconfirm>
        </Space>
      ),
    },
  ]

  return (
    <Card>
      <div className="flex justify-between mb-4">
        <Input.Search
          placeholder="Tim kiem nha cung cap..." allowClear style={{ width: 300 }}
          onSearch={setSearch} prefix={<SearchOutlined />}
        />
        <Button type="primary" icon={<PlusOutlined />} onClick={() => { setEditing(null); form.resetFields(); setModalOpen(true) }}>
          Them nha cung cap
        </Button>
      </div>
      <Table dataSource={suppliers} columns={columns} rowKey="id" loading={loading} size="middle" />
      <Modal title={editing ? 'Sua nha cung cap' : 'Them nha cung cap'} open={modalOpen} onCancel={() => setModalOpen(false)} footer={null}>
        <Form form={form} layout="vertical" onFinish={handleSave}>
          <Form.Item name="code" label="Ma NCC" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="name" label="Ten NCC" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="contact_person" label="Nguoi lien he"><Input /></Form.Item>
          <Form.Item name="phone" label="So dien thoai"><Input /></Form.Item>
          <Form.Item name="email" label="Email"><Input /></Form.Item>
          <Form.Item name="address" label="Dia chi"><Input.TextArea rows={2} /></Form.Item>
          <Button type="primary" htmlType="submit" block>{editing ? 'Cap nhat' : 'Them moi'}</Button>
        </Form>
      </Modal>
    </Card>
  )
}

function MaterialTab() {
  const [materials, setMaterials] = useState<Material[]>([])
  const [suppliers, setSuppliers] = useState<Supplier[]>([])
  const [loading, setLoading] = useState(false)
  const [modalOpen, setModalOpen] = useState(false)
  const [form] = Form.useForm()

  const fetchData = async () => {
    setLoading(true)
    try {
      const [mRes, sRes] = await Promise.all([api.get('/iqc/materials'), api.get('/iqc/suppliers')])
      setMaterials(mRes.data); setSuppliers(sRes.data)
    } catch { message.error('Loi tai du lieu') }
    finally { setLoading(false) }
  }

  useEffect(() => { fetchData() }, [])

  const handleSave = async (values: any) => {
    try {
      await api.post('/iqc/materials', values)
      message.success('Them nguyen lieu thanh cong')
      setModalOpen(false); form.resetFields(); fetchData()
    } catch (err: any) { message.error(err.response?.data?.detail || 'Loi') }
  }

  const columns = [
    { title: 'Ma NL', dataIndex: 'code', key: 'code', width: 100 },
    { title: 'Ten nguyen lieu', dataIndex: 'name', key: 'name' },
    { title: 'Dac tinh', dataIndex: 'specification', key: 'specification' },
    { title: 'Don vi', dataIndex: 'unit', key: 'unit', width: 80 },
    { title: 'Nha cung cap', key: 'supplier', render: (_: any, r: Material) => r.supplier?.name },
    { title: 'Thao tac', key: 'actions', width: 100,
      render: (_: any, r: Material) => (
        <Popconfirm title="Xoa nguyen lieu nay?" onConfirm={async () => { await api.delete(`/iqc/materials/${r.id}`); fetchData() }}>
          <Button size="small" danger icon={<DeleteOutlined />} />
        </Popconfirm>
      ),
    },
  ]

  return (
    <Card>
      <div className="flex justify-end mb-4 gap-2">
        <Upload
          accept=".xlsx"
          showUploadList={false}
          customRequest={async (options: any) => {
            const formData = new FormData()
            formData.append('file', options.file)
            try {
              const res = await api.post('/import/materials', formData)
              message.success(res.data.message)
              fetchData()
            } catch (err: any) { message.error(err.response?.data?.detail || 'Loi import') }
          }}
        >
          <Button icon={<UploadOutlined />}>Import Excel</Button>
        </Upload>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => { form.resetFields(); setModalOpen(true) }}>
          Them nguyen lieu
        </Button>
      </div>
      <Table dataSource={materials} columns={columns} rowKey="id" loading={loading} size="middle" />
      <Modal title="Them nguyen lieu" open={modalOpen} onCancel={() => setModalOpen(false)} footer={null}>
        <Form form={form} layout="vertical" onFinish={handleSave}>
          <Form.Item name="code" label="Ma NL" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="name" label="Ten NL" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="specification" label="Dac tinh ky thuat"><Input.TextArea rows={2} /></Form.Item>
          <Form.Item name="unit" label="Don vi" initialValue="pcs"><Input /></Form.Item>
          <Form.Item name="supplier_id" label="Nha cung cap" rules={[{ required: true }]}>
            <Select options={suppliers.map(s => ({ label: s.name, value: s.id }))} />
          </Form.Item>
          <Button type="primary" htmlType="submit" block>Them moi</Button>
        </Form>
      </Modal>
    </Card>
  )
}

function InspectionTab() {
  const [inspections, setInspections] = useState<IQCInspection[]>([])
  const [loading, setLoading] = useState(false)
  const [createOpen, setCreateOpen] = useState(false)
  const [detailOpen, setDetailOpen] = useState(false)
  const [selected, setSelected] = useState<IQCInspection | null>(null)
  const [resultOpen, setResultOpen] = useState(false)
  const [form] = Form.useForm()
  const [resultForm] = Form.useForm()
  const [materials, setMaterials] = useState<Material[]>([])
  const [suppliers, setSuppliers] = useState<Supplier[]>([])
  const [users, setUsers] = useState<{ id: number; full_name: string }[]>([])
  const [aqlData, setAqlData] = useState<any>(null)
  const [checklists, setChecklists] = useState<{ id: number; name: string; items: any[] }[]>([])
  const [selectedChecklist, setSelectedChecklist] = useState<number | null>(null)

  const fetchInspections = async () => {
    setLoading(true)
    try {
      const [iRes, mRes, sRes, uRes, aqlRes, cRes] = await Promise.all([
        api.get('/iqc/inspections'), api.get('/iqc/materials'), api.get('/iqc/suppliers'),
        api.get('/users/lookup'), api.get('/aql-table'),
        api.get('/checklists/', { params: { module: 'iqc' } }),
      ])
      setInspections(iRes.data); setMaterials(mRes.data); setSuppliers(sRes.data)
      setUsers(uRes.data); setAqlData(aqlRes.data); setChecklists(cRes.data)
    } catch { message.error('Loi tai du lieu') }
    finally { setLoading(false) }
  }

  useEffect(() => { fetchInspections() }, [])

  const handleCreate = async (values: any) => {
    try {
      const res = await api.post('/iqc/inspections', { ...values, inspection_date: values.inspection_date.toISOString() })
      const inspId = res.data.id
      const cl = checklists.find(c => c.id === selectedChecklist)
      if (cl && cl.items) {
        for (const item of cl.items) {
          await api.post(`/iqc/inspections/${inspId}/results`, {
            item_name: item.item_name,
            specification: item.specification || '',
            measured_value: 0,
            standard_min: item.standard_min || null,
            standard_max: item.standard_max || null,
            result: 'pass',
          })
        }
      }
      message.success('Tao phieu kiem tra thanh cong')
      setCreateOpen(false); form.resetFields(); setSelectedChecklist(null); fetchInspections()
    } catch (err: any) { message.error(err.response?.data?.detail || 'Loi') }
  }

  const handleAddResult = async (values: any) => {
    if (!selected) return
    try {
      await api.post(`/iqc/inspections/${selected.id}/results`, values)
      message.success('Them ket qua thanh cong')
      setResultOpen(false); resultForm.resetFields(); fetchInspections()
    } catch (err: any) { message.error(err.response?.data?.detail || 'Loi') }
  }

  const handleStatusChange = async (id: number, status: string) => {
    await api.put(`/iqc/inspections/${id}/status`, null, { params: { status } })
    message.success('Cap nhat trang thai thanh cong')
    fetchInspections()
  }

  const statusTag = (status: string) => {
    const colors: Record<string, string> = { pending: 'orange', pass: 'green', fail: 'red' }
    const labels: Record<string, string> = { pending: 'Cho kiem', pass: 'Dat', fail: 'Khong dat' }
    return <Tag color={colors[status]}>{labels[status]}</Tag>
  }

  const columns = [
    { title: 'So phieu', dataIndex: 'inspection_no', key: 'inspection_no', width: 120 },
    { title: 'Nguyen lieu', key: 'material', render: (_: any, r: IQCInspection) => r.material?.name },
    { title: 'NCC', key: 'supplier', render: (_: any, r: IQCInspection) => r.supplier?.name },
    { title: 'Lo', dataIndex: 'lot_no', key: 'lot_no', width: 100 },
    { title: 'SL/Sample', key: 'qty', width: 100, render: (_: any, r: IQCInspection) => `${r.quantity}/${r.sample_size}` },
    { title: 'Ngay kiem', key: 'date', width: 120, render: (_: any, r: IQCInspection) => dayjs(r.inspection_date).format('DD/MM/YYYY') },
    { title: 'Trang thai', key: 'status', width: 120, render: (_: any, r: IQCInspection) => statusTag(r.status) },
    {
      title: 'Thao tac', key: 'actions', width: 280,
      render: (_: any, r: IQCInspection) => (
        <Space>
          <Button size="small" icon={<EyeOutlined />} onClick={() => { setSelected(r); setDetailOpen(true) }}>Chi tiet</Button>
          {r.status === 'pending' && (
            <>
              <Button size="small" type="primary" onClick={() => handleStatusChange(r.id, 'pass')}>Dat</Button>
              <Button size="small" danger onClick={() => handleStatusChange(r.id, 'fail')}>Khong dat</Button>
            </>
          )}
        </Space>
      ),
    },
  ]

  return (
    <Card>
      <div className="flex justify-end mb-4 gap-2">
        <Button icon={<DownloadOutlined />} onClick={() => window.open('/api/export/inspections?module=iqc')}>
          Xuat Excel
        </Button>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => { form.resetFields(); setCreateOpen(true) }}>
          Tao phieu kiem tra
        </Button>
      </div>
      <Table dataSource={inspections} columns={columns} rowKey="id" loading={loading} size="middle" />

      <Modal title="Tao phieu kiem tra IQC" open={createOpen} onCancel={() => setCreateOpen(false)} footer={null} width={600}>
        <AQLHelper aqlData={aqlData} />
        <Form form={form} layout="vertical" onFinish={handleCreate}>
          <Form.Item name="inspection_no" label="So phieu" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="material_id" label="Nguyen lieu" rules={[{ required: true }]}>
            <Select options={materials.map(m => ({ label: m.name, value: m.id }))} />
          </Form.Item>
          <Form.Item name="supplier_id" label="Nha cung cap" rules={[{ required: true }]}>
            <Select options={suppliers.map(s => ({ label: s.name, value: s.id }))} />
          </Form.Item>
          <Form.Item name="lot_no" label="So lo" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="quantity" label="So luong" rules={[{ required: true }]}><InputNumber min={0} className="w-full" /></Form.Item>
          <Form.Item name="sample_size" label="Co mau" rules={[{ required: true }]}><InputNumber min={1} className="w-full" /></Form.Item>
          <Form.Item name="inspection_date" label="Ngay kiem" rules={[{ required: true }]}><DatePicker showTime className="w-full" /></Form.Item>
          <Form.Item name="inspector_id" label="Nguoi kiem" rules={[{ required: true }]}>
            <Select showSearch optionFilterProp="label" placeholder="Chon nguoi kiem" options={users.map(u => ({ label: u.full_name, value: u.id }))} />
          </Form.Item>
          <Form.Item label="Checklist mau (tu dong dien muc kiem)">
            <Select
              allowClear
              placeholder="Chon checklist co san..."
              value={selectedChecklist}
              onChange={setSelectedChecklist}
              options={checklists.map(c => ({ label: `${c.name} (${c.items?.length || 0} muc)`, value: c.id }))}
            />
          </Form.Item>
          <Form.Item name="notes" label="Ghi chu"><Input.TextArea rows={2} /></Form.Item>
          <Button type="primary" htmlType="submit" block>Tao phieu</Button>
        </Form>
      </Modal>

      <Modal title="Chi tiet phieu kiem tra" open={detailOpen} onCancel={() => setDetailOpen(false)} footer={null} width={700}>
        {selected && (
          <div>
            <Descriptions column={2} bordered size="small" className="mb-4">
              <Descriptions.Item label="So phieu">{selected.inspection_no}</Descriptions.Item>
              <Descriptions.Item label="Trang thai">{statusTag(selected.status)}</Descriptions.Item>
              <Descriptions.Item label="Nguyen lieu">{selected.material?.name}</Descriptions.Item>
              <Descriptions.Item label="NCC">{selected.supplier?.name}</Descriptions.Item>
              <Descriptions.Item label="So lo">{selected.lot_no}</Descriptions.Item>
              <Descriptions.Item label="SL">{selected.quantity} / Sample: {selected.sample_size}</Descriptions.Item>
              <Descriptions.Item label="Ngay kiem">{dayjs(selected.inspection_date).format('DD/MM/YYYY HH:mm')}</Descriptions.Item>
              <Descriptions.Item label="Nguoi kiem">{selected.inspector?.full_name}</Descriptions.Item>
            </Descriptions>
            <div className="flex justify-between items-center mb-2">
              <h4 className="font-bold">Ket qua kiem tra</h4>
              <Button type="primary" size="small" icon={<PlusOutlined />} onClick={() => { resultForm.resetFields(); setResultOpen(true) }}>
                Them ket qua
              </Button>
            </div>
            <Table
              dataSource={selected.results}
              rowKey="id"
              size="small"
              pagination={false}
              columns={[
                { title: 'Muc kiem', dataIndex: 'item_name' },
                { title: 'Tieu chuan', dataIndex: 'specification' },
                { title: 'Gia tri do', dataIndex: 'measured_value' },
                { title: 'Min', dataIndex: 'standard_min' },
                { title: 'Max', dataIndex: 'standard_max' },
                { title: 'Ket qua', dataIndex: 'result', render: (v: string) => <Tag color={v === 'pass' ? 'green' : 'red'}>{v === 'pass' ? 'Dat' : 'Khong dat'}</Tag> },
              ]}
            />
          </div>
        )}
      </Modal>

      <Modal title="Them ket qua kiem tra" open={resultOpen} onCancel={() => setResultOpen(false)} footer={null}>
        <Form form={resultForm} layout="vertical" onFinish={handleAddResult}>
          <Form.Item name="item_name" label="Muc kiem" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="specification" label="Tieu chuan"><Input /></Form.Item>
          <Form.Item name="measured_value" label="Gia tri do" rules={[{ required: true }]}><InputNumber className="w-full" /></Form.Item>
          <Form.Item name="standard_min" label="Gioi han duoi"><InputNumber className="w-full" /></Form.Item>
          <Form.Item name="standard_max" label="Gioi han tren"><InputNumber className="w-full" /></Form.Item>
          <Form.Item name="result" label="Ket qua" initialValue="pass">
            <Select options={[{ label: 'Dat', value: 'pass' }, { label: 'Khong dat', value: 'fail' }]} />
          </Form.Item>
          <Form.Item name="notes" label="Ghi chu"><Input.TextArea rows={2} /></Form.Item>
          <Button type="primary" htmlType="submit" block>Them ket qua</Button>
        </Form>
      </Modal>
    </Card>
  )
}
