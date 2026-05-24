import { useEffect, useState } from 'react'
import {
  Table, Button, Modal, Form, Input, Space, message, Card,
  Select, InputNumber, DatePicker, Tag, Descriptions,
} from 'antd'
import { PlusOutlined, EyeOutlined, DeleteOutlined, DownloadOutlined } from '@ant-design/icons'
import api from '../services/api'
import dayjs from 'dayjs'

interface IPQCResult {
  id: number; item_name: string; specification: string | null
  measured_value: number; standard_min: number | null; standard_max: number | null
  result: string; notes: string | null
}

interface IPQCInspection {
  id: number; inspection_no: string; process_name: string; work_center: string
  machine: string | null; shift: string; inspection_date: string
  inspector_id: number; sample_size: number; status: string; notes: string | null
  inspector: any; results: IPQCResult[]
}

export default function IPQCPage() {
  const [inspections, setInspections] = useState<IPQCInspection[]>([])
  const [loading, setLoading] = useState(false)
  const [createOpen, setCreateOpen] = useState(false)
  const [detailOpen, setDetailOpen] = useState(false)
  const [selected, setSelected] = useState<IPQCInspection | null>(null)
  const [resultOpen, setResultOpen] = useState(false)
  const [form] = Form.useForm()
  const [resultForm] = Form.useForm()
  const [users, setUsers] = useState<{ id: number; full_name: string }[]>([])

  const fetchData = async () => {
    setLoading(true)
    try {
      const [res, uRes] = await Promise.all([api.get('/ipqc/inspections'), api.get('/users/lookup')])
      setInspections(res.data); setUsers(uRes.data)
    }
    catch { message.error('Loi tai du lieu') }
    finally { setLoading(false) }
  }

  useEffect(() => { fetchData() }, [])

  const handleCreate = async (values: any) => {
    try {
      await api.post('/ipqc/inspections', { ...values, inspection_date: values.inspection_date.toISOString() })
      message.success('Tao phieu kiem tra thanh cong')
      setCreateOpen(false); form.resetFields(); fetchData()
    } catch (err: any) { message.error(err.response?.data?.detail || 'Loi') }
  }

  const handleAddResult = async (values: any) => {
    if (!selected) return
    try {
      await api.post(`/ipqc/inspections/${selected.id}/results`, values)
      message.success('Them ket qua thanh cong')
      setResultOpen(false); resultForm.resetFields(); fetchData()
    } catch (err: any) { message.error(err.response?.data?.detail || 'Loi') }
  }

  const handleStatusChange = async (id: number, status: string) => {
    await api.put(`/ipqc/inspections/${id}/status`, null, { params: { status } })
    message.success('Cap nhat trang thai thanh cong')
    fetchData()
  }

  const handleDeleteResult = async (resultId: number) => {
    await api.delete(`/ipqc/results/${resultId}`)
    message.success('Xoa ket qua thanh cong')
    fetchData()
  }

  const statusTag = (status: string) => {
    const m: Record<string, { color: string; label: string }> = {
      pending: { color: 'orange', label: 'Cho kiem' },
      pass: { color: 'green', label: 'Dat' },
      fail: { color: 'red', label: 'Khong dat' },
    }
    return <Tag color={m[status]?.color}>{m[status]?.label}</Tag>
  }

  const columns = [
    { title: 'So phieu', dataIndex: 'inspection_no', key: 'no', width: 120 },
    { title: 'Cong doan', dataIndex: 'process_name', key: 'process' },
    { title: 'Tram', dataIndex: 'work_center', key: 'wc', width: 100 },
    { title: 'May', dataIndex: 'machine', key: 'machine', width: 80 },
    { title: 'Ca', dataIndex: 'shift', key: 'shift', width: 70 },
    { title: 'Sample', dataIndex: 'sample_size', key: 'sample', width: 70 },
    { title: 'Ngay kiem', key: 'date', width: 100, render: (_: any, r: IPQCInspection) => dayjs(r.inspection_date).format('DD/MM/YYYY') },
    { title: 'Trang thai', key: 'status', width: 110, render: (_: any, r: IPQCInspection) => statusTag(r.status) },
    {
      title: 'Thao tac', key: 'actions', width: 250,
      render: (_: any, r: IPQCInspection) => (
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
    <div>
      <h2 className="text-xl font-bold mb-4">Kiem tra chat luong trong qua trinh (IPQC)</h2>
      <Card>
        <div className="flex justify-end mb-4 gap-2">
          <Button icon={<DownloadOutlined />} onClick={() => window.open('/api/export/inspections?module=ipqc')}>
            Xuat Excel
          </Button>
          <Button type="primary" icon={<PlusOutlined />} onClick={() => { form.resetFields(); setCreateOpen(true) }}>
            Tao phieu kiem tra
          </Button>
        </div>
        <Table dataSource={inspections} columns={columns} rowKey="id" loading={loading} size="middle" />

        <Modal title="Tao phieu kiem tra IPQC" open={createOpen} onCancel={() => setCreateOpen(false)} footer={null} width={600}>
          <Form form={form} layout="vertical" onFinish={handleCreate}>
            <Form.Item name="inspection_no" label="So phieu" rules={[{ required: true }]}><Input /></Form.Item>
            <Form.Item name="process_name" label="Cong doan" rules={[{ required: true }]}><Input placeholder="VD: Han, Tien, Lap rap..." /></Form.Item>
            <Form.Item name="work_center" label="Tram lam viec" rules={[{ required: true }]}><Input placeholder="VD: Tram 1, Line A..." /></Form.Item>
            <Form.Item name="machine" label="May"><Input placeholder="VD: May tien CNC-01..." /></Form.Item>
            <Form.Item name="shift" label="Ca" initialValue="Ca 1">
              <Select options={['Ca 1', 'Ca 2', 'Ca 3'].map(s => ({ label: s, value: s }))} />
            </Form.Item>
            <Form.Item name="sample_size" label="Co mau" initialValue={5} rules={[{ required: true }]}>
              <InputNumber min={1} max={25} className="w-full" />
            </Form.Item>
            <Form.Item name="inspection_date" label="Ngay kiem" rules={[{ required: true }]}>
              <DatePicker showTime className="w-full" />
            </Form.Item>
            <Form.Item name="inspector_id" label="Nguoi kiem" rules={[{ required: true }]}>
              <Select showSearch optionFilterProp="label" placeholder="Chon nguoi kiem" options={users.map(u => ({ label: u.full_name, value: u.id }))} />
            </Form.Item>
            <Form.Item name="notes" label="Ghi chu"><Input.TextArea rows={2} /></Form.Item>
            <Button type="primary" htmlType="submit" block>Tao phieu</Button>
          </Form>
        </Modal>

        <Modal title="Chi tiet phieu IPQC" open={detailOpen} onCancel={() => setDetailOpen(false)} footer={null} width={700}>
          {selected && (
            <div>
              <Descriptions column={2} bordered size="small" className="mb-4">
                <Descriptions.Item label="So phieu">{selected.inspection_no}</Descriptions.Item>
                <Descriptions.Item label="Trang thai">{statusTag(selected.status)}</Descriptions.Item>
                <Descriptions.Item label="Cong doan">{selected.process_name}</Descriptions.Item>
                <Descriptions.Item label="Tram">{selected.work_center}</Descriptions.Item>
                <Descriptions.Item label="May">{selected.machine || '-'}</Descriptions.Item>
                <Descriptions.Item label="Ca">{selected.shift}</Descriptions.Item>
                <Descriptions.Item label="Co mau">{selected.sample_size}</Descriptions.Item>
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
                  {
                    title: '', key: 'del', width: 50,
                    render: (_: any, rr: IPQCResult) => (
                      <Button size="small" danger icon={<DeleteOutlined />} onClick={() => handleDeleteResult(rr.id)} />
                    ),
                  },
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
    </div>
  )
}
