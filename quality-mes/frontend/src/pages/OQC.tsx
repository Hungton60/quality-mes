import { useEffect, useState } from 'react'
import {
  Table, Button, Modal, Form, Input, Space, message, Popconfirm, Tabs, Card,
  Select, InputNumber, DatePicker, Tag, Descriptions, Upload,
} from 'antd'
import { PlusOutlined, DeleteOutlined, EyeOutlined, DownloadOutlined, UploadOutlined } from '@ant-design/icons'
import api from '../services/api'
import dayjs from 'dayjs'

interface Product {
  id: number; code: string; name: string; specification: string | null; unit: string
}

interface OQCResult {
  id: number; item_name: string; specification: string | null
  measured_value: number; standard_min: number | null; standard_max: number | null
  result: string; notes: string | null
}

interface OQCInspection {
  id: number; inspection_no: string; product_id: number; lot_no: string
  quantity: number; sample_size: number; inspection_date: string
  inspector_id: number; status: string; notes: string | null
  product: Product | null; inspector: any; results: OQCResult[]
}

export default function OQCPage() {
  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Kiem tra chat luong thanh pham (OQC)</h2>
      <Tabs
        items={[
          { key: 'inspections', label: 'Phieu kiem tra', children: <InspectionTab /> },
          { key: 'products', label: 'San pham', children: <ProductTab /> },
        ]}
      />
    </div>
  )
}

function ProductTab() {
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(false)
  const [modalOpen, setModalOpen] = useState(false)
  const [form] = Form.useForm()

  const fetchProducts = async () => {
    setLoading(true)
    try { const res = await api.get('/oqc/products'); setProducts(res.data) }
    catch { message.error('Loi tai danh sach san pham') }
    finally { setLoading(false) }
  }

  useEffect(() => { fetchProducts() }, [])

  const handleSave = async (values: any) => {
    try {
      await api.post('/oqc/products', values)
      message.success('Them san pham thanh cong')
      setModalOpen(false); form.resetFields(); fetchProducts()
    } catch (err: any) { message.error(err.response?.data?.detail || 'Loi') }
  }

  const columns = [
    { title: 'Ma SP', dataIndex: 'code', key: 'code', width: 100 },
    { title: 'Ten san pham', dataIndex: 'name', key: 'name' },
    { title: 'Dac tinh', dataIndex: 'specification', key: 'specification' },
    { title: 'Don vi', dataIndex: 'unit', key: 'unit', width: 80 },
    { title: 'Thao tac', key: 'actions', width: 100,
      render: (_: any, r: Product) => (
        <Popconfirm title="Xoa san pham nay?" onConfirm={async () => { await api.delete(`/oqc/products/${r.id}`); fetchProducts() }}>
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
              const res = await api.post('/import/products', formData)
              message.success(res.data.message)
              fetchProducts()
            } catch (err: any) { message.error(err.response?.data?.detail || 'Loi import') }
          }}
        >
          <Button icon={<UploadOutlined />}>Import Excel</Button>
        </Upload>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => { form.resetFields(); setModalOpen(true) }}>
          Them san pham
        </Button>
      </div>
      <Table dataSource={products} columns={columns} rowKey="id" loading={loading} size="middle" />
      <Modal title="Them san pham" open={modalOpen} onCancel={() => setModalOpen(false)} footer={null}>
        <Form form={form} layout="vertical" onFinish={handleSave}>
          <Form.Item name="code" label="Ma SP" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="name" label="Ten SP" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="specification" label="Dac tinh"><Input.TextArea rows={2} /></Form.Item>
          <Form.Item name="unit" label="Don vi" initialValue="pcs"><Input /></Form.Item>
          <Button type="primary" htmlType="submit" block>Them moi</Button>
        </Form>
      </Modal>
    </Card>
  )
}

function InspectionTab() {
  const [inspections, setInspections] = useState<OQCInspection[]>([])
  const [loading, setLoading] = useState(false)
  const [createOpen, setCreateOpen] = useState(false)
  const [detailOpen, setDetailOpen] = useState(false)
  const [selected, setSelected] = useState<OQCInspection | null>(null)
  const [resultOpen, setResultOpen] = useState(false)
  const [form] = Form.useForm()
  const [resultForm] = Form.useForm()
  const [products, setProducts] = useState<Product[]>([])
  const [users, setUsers] = useState<{ id: number; full_name: string }[]>([])
  const [checklists, setChecklists] = useState<{ id: number; name: string; items: any[] }[]>([])
  const [selectedChecklist, setSelectedChecklist] = useState<number | null>(null)

  const fetchData = async () => {
    setLoading(true)
    try {
      const [iRes, pRes, uRes, cRes] = await Promise.all([
        api.get('/oqc/inspections'), api.get('/oqc/products'), api.get('/users/lookup'),
        api.get('/checklists/', { params: { module: 'oqc' } }),
      ])
      setInspections(iRes.data); setProducts(pRes.data); setUsers(uRes.data); setChecklists(cRes.data)
    } catch { message.error('Loi tai du lieu') }
    finally { setLoading(false) }
  }

  useEffect(() => { fetchData() }, [])

  const handleCreate = async (values: any) => {
    try {
      const res = await api.post('/oqc/inspections', { ...values, inspection_date: values.inspection_date.toISOString() })
      const inspId = res.data.id
      const cl = checklists.find(c => c.id === selectedChecklist)
      if (cl && cl.items) {
        for (const item of cl.items) {
          await api.post(`/oqc/inspections/${inspId}/results`, {
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
      setCreateOpen(false); form.resetFields(); setSelectedChecklist(null); fetchData()
    } catch (err: any) { message.error(err.response?.data?.detail || 'Loi') }
  }

  const handleAddResult = async (values: any) => {
    if (!selected) return
    try {
      await api.post(`/oqc/inspections/${selected.id}/results`, values)
      message.success('Them ket qua thanh cong')
      setResultOpen(false); resultForm.resetFields(); fetchData()
    } catch (err: any) { message.error(err.response?.data?.detail || 'Loi') }
  }

  const handleStatusChange = async (id: number, status: string) => {
    await api.put(`/oqc/inspections/${id}/status`, null, { params: { status } })
    message.success('Cap nhat trang thai thanh cong')
    fetchData()
  }

  const statusTag = (status: string) => {
    const colors: Record<string, string> = { pending: 'orange', pass: 'green', fail: 'red' }
    const labels: Record<string, string> = { pending: 'Cho kiem', pass: 'Dat', fail: 'Khong dat' }
    return <Tag color={colors[status]}>{labels[status]}</Tag>
  }

  const columns = [
    { title: 'So phieu', dataIndex: 'inspection_no', key: 'inspection_no', width: 120 },
    { title: 'San pham', key: 'product', render: (_: any, r: OQCInspection) => r.product?.name },
    { title: 'Lo', dataIndex: 'lot_no', key: 'lot_no', width: 100 },
    { title: 'SL/Sample', key: 'qty', width: 100, render: (_: any, r: OQCInspection) => `${r.quantity}/${r.sample_size}` },
    { title: 'Ngay kiem', key: 'date', width: 120, render: (_: any, r: OQCInspection) => dayjs(r.inspection_date).format('DD/MM/YYYY') },
    { title: 'Trang thai', key: 'status', width: 120, render: (_: any, r: OQCInspection) => statusTag(r.status) },
    {
      title: 'Thao tac', key: 'actions', width: 280,
      render: (_: any, r: OQCInspection) => (
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
        <Button icon={<DownloadOutlined />} onClick={() => window.open('/api/export/inspections?module=oqc')}>
          Xuat Excel
        </Button>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => { form.resetFields(); setCreateOpen(true) }}>
          Tao phieu kiem tra
        </Button>
      </div>
      <Table dataSource={inspections} columns={columns} rowKey="id" loading={loading} size="middle" />

      <Modal title="Tao phieu kiem tra OQC" open={createOpen} onCancel={() => setCreateOpen(false)} footer={null} width={600}>
        <Form form={form} layout="vertical" onFinish={handleCreate}>
          <Form.Item name="inspection_no" label="So phieu" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="product_id" label="San pham" rules={[{ required: true }]}>
            <Select options={products.map(p => ({ label: p.name, value: p.id }))} />
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

      <Modal title="Chi tiet phieu kiem tra OQC" open={detailOpen} onCancel={() => setDetailOpen(false)} footer={null} width={700}>
        {selected && (
          <div>
            <Descriptions column={2} bordered size="small" className="mb-4">
              <Descriptions.Item label="So phieu">{selected.inspection_no}</Descriptions.Item>
              <Descriptions.Item label="Trang thai">{statusTag(selected.status)}</Descriptions.Item>
              <Descriptions.Item label="San pham">{selected.product?.name}</Descriptions.Item>
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
