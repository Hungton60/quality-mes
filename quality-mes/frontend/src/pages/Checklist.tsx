import { useEffect, useState } from 'react'
import { Table, Button, Modal, Form, Input, Space, message, Popconfirm, Card, Select, Tag, InputNumber, Upload } from 'antd'
import { PlusOutlined, DeleteOutlined, EditOutlined, UploadOutlined } from '@ant-design/icons'
import api from '../services/api'

interface Checklist {
  id: number; code: string; name: string; module: string
  items: { item_name: string; specification: string; standard_min: number | null; standard_max: number | null }[]
}

const moduleLabels: Record<string, string> = { iqc: 'IQC', oqc: 'OQC', ipqc: 'IPQC' }

export default function ChecklistPage() {
  const [templates, setTemplates] = useState<Checklist[]>([])
  const [loading, setLoading] = useState(false)
  const [modalOpen, setModalOpen] = useState(false)
  const [editing, setEditing] = useState<Checklist | null>(null)
  const [items, setItems] = useState<{ item_name: string; specification: string; standard_min: number | null; standard_max: number | null }[]>([
    { item_name: '', specification: '', standard_min: null, standard_max: null },
  ])
  const [form] = Form.useForm()
  const [moduleFilter, setModuleFilter] = useState<string | undefined>()

  const fetchData = async () => {
    setLoading(true)
    try {
      const params: any = {}
      if (moduleFilter) params.module = moduleFilter
      const res = await api.get('/checklists/', { params })
      setTemplates(res.data)
    } catch { message.error('Loi tai du lieu') }
    finally { setLoading(false) }
  }

  useEffect(() => { fetchData() }, [moduleFilter])

  const handleSave = async () => {
    const values = form.getFieldsValue()
    const validItems = items.filter(i => i.item_name.trim())
    if (!values.code || !values.name || validItems.length === 0) {
      message.error('Vui long nhap day du: Ma, Ten va it nhat 1 muc kiem')
      return
    }
    try {
      const payload = { ...values, items: validItems }
      if (editing) {
        await api.put(`/checklists/${editing.id}`, payload)
        message.success('Cap nhat checklist thanh cong')
      } else {
        await api.post('/checklists/', payload)
        message.success('Tao checklist thanh cong')
      }
      setModalOpen(false)
      setEditing(null)
      form.resetFields()
      setItems([{ item_name: '', specification: '', standard_min: null, standard_max: null }])
      fetchData()
    } catch (err: any) { message.error(err.response?.data?.detail || 'Loi') }
  }

  const handleDelete = async (id: number) => {
    await api.delete(`/checklists/${id}`)
    message.success('Xoa thanh cong')
    fetchData()
  }

  const openEdit = (t: Checklist) => {
    setEditing(t)
    form.setFieldsValue({ code: t.code, name: t.name, module: t.module })
    setItems(t.items.length > 0 ? t.items : [{ item_name: '', specification: '', standard_min: null, standard_max: null }])
    setModalOpen(true)
  }

  const addItem = () => {
    setItems([...items, { item_name: '', specification: '', standard_min: null, standard_max: null }])
  }

  const updateItem = (idx: number, field: string, value: any) => {
    const newItems = [...items]
    newItems[idx] = { ...newItems[idx], [field]: value }
    setItems(newItems)
  }

  const removeItem = (idx: number) => {
    if (items.length === 1) return
    setItems(items.filter((_, i) => i !== idx))
  }

  const columns = [
    { title: 'Ma', dataIndex: 'code', key: 'code', width: 120 },
    { title: 'Ten checklist', dataIndex: 'name', key: 'name' },
    { title: 'Module', dataIndex: 'module', key: 'module', width: 80, render: (v: string) => <Tag>{moduleLabels[v] || v}</Tag> },
    { title: 'So muc kiem', key: 'count', width: 100, render: (_: any, r: Checklist) => r.items?.length || 0 },
    {
      title: '', key: 'actions', width: 100,
      render: (_: any, r: Checklist) => (
        <Space>
          <Button size="small" icon={<EditOutlined />} onClick={() => openEdit(r)} />
          <Popconfirm title="Xoa checklist nay?" onConfirm={() => handleDelete(r.id)}>
            <Button size="small" danger icon={<DeleteOutlined />} />
          </Popconfirm>
        </Space>
      ),
    },
  ]

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Quan ly Checklist mau</h2>
      <Card>
        <div className="flex justify-between mb-4">
          <Select
            allowClear placeholder="Loc module" style={{ width: 150 }}
            value={moduleFilter} onChange={setModuleFilter}
            options={Object.entries(moduleLabels).map(([k, v]) => ({ label: v, value: k }))}
          />
          <Button type="primary" icon={<PlusOutlined />} onClick={() => {
            setEditing(null)
            form.resetFields()
            setItems([{ item_name: '', specification: '', standard_min: null, standard_max: null }])
            setModalOpen(true)
          }}>
            Tao checklist moi
          </Button>
          <Upload
            accept=".xlsx"
            showUploadList={false}
            customRequest={async (options: any) => {
              const formData = new FormData()
              formData.append('file', options.file)
              try {
                const res = await api.post(`/checklists/import-excel?module=${moduleFilter || 'iqc'}`, formData)
                message.success(res.data.message)
                fetchData()
              } catch (err: any) { message.error(err.response?.data?.detail || 'Loi import') }
            }}
          >
            <Button icon={<UploadOutlined />}>Import Excel</Button>
          </Upload>
        </div>
        <Table dataSource={templates} columns={columns} rowKey="id" loading={loading} size="middle" />

        <Modal
          title={editing ? 'Sua checklist' : 'Tao checklist moi'}
          open={modalOpen}
          onCancel={() => setModalOpen(false)}
          onOk={handleSave}
          okText={editing ? 'Cap nhat' : 'Tao moi'}
          width={700}
        >
          <Form form={form} layout="vertical">
            <Space className="w-full" size="middle">
              <Form.Item name="code" label="Ma checklist" rules={[{ required: true }]} style={{ width: 150 }}>
                <Input placeholder="VD: IQC-THEP" />
              </Form.Item>
              <Form.Item name="name" label="Ten checklist" rules={[{ required: true }]} style={{ width: 250 }}>
                <Input placeholder="VD: Kiem tra thep tam 2mm" />
              </Form.Item>
              <Form.Item name="module" label="Module" rules={[{ required: true }]} style={{ width: 120 }} initialValue="iqc">
                <Select options={Object.entries(moduleLabels).map(([k, v]) => ({ label: v, value: k }))} />
              </Form.Item>
            </Space>
          </Form>

          <h4 className="mb-2">Danh sach muc kiem</h4>
          {items.map((item, idx) => (
            <div key={idx} className="flex gap-2 mb-2 items-start">
              <Input
                placeholder="Muc kiem" value={item.item_name}
                onChange={e => updateItem(idx, 'item_name', e.target.value)}
                style={{ flex: 2 }}
              />
              <Input
                placeholder="Tieu chuan" value={item.specification}
                onChange={e => updateItem(idx, 'specification', e.target.value)}
                style={{ flex: 2 }}
              />
              <InputNumber
                placeholder="Min" value={item.standard_min}
                onChange={v => updateItem(idx, 'standard_min', v)}
                style={{ width: 90 }}
              />
              <InputNumber
                placeholder="Max" value={item.standard_max}
                onChange={v => updateItem(idx, 'standard_max', v)}
                style={{ width: 90 }}
              />
              <Button danger icon={<DeleteOutlined />} onClick={() => removeItem(idx)} disabled={items.length === 1} />
            </div>
          ))}
          <Button type="dashed" onClick={addItem} block className="mt-2">
            + Them muc kiem
          </Button>
        </Modal>
      </Card>
    </div>
  )
}
