import { useEffect, useState } from 'react'
import { Table, Button, Modal, Form, Input, Space, message, Popconfirm, Card, Select, InputNumber, DatePicker, Tag } from 'antd'
import { PlusOutlined, DeleteOutlined, ToolOutlined } from '@ant-design/icons'
import api from '../services/api'
import dayjs from 'dayjs'

interface Equipment {
  id: number; code: string; name: string; type: string; serial_no: string | null
  location: string | null; calibration_interval_days: number
  last_calibration_date: string | null; next_calibration_date: string | null
  status: string; notes: string | null
  days_until_calibration: number | null; calibration_overdue: boolean
}

export default function EquipmentPage() {
  const [items, setItems] = useState<Equipment[]>([])
  const [loading, setLoading] = useState(false)
  const [modalOpen, setModalOpen] = useState(false)
  const [calModal, setCalModal] = useState<Equipment | null>(null)
  const [form] = Form.useForm()
  const [calForm] = Form.useForm()

  const fetchData = async () => {
    setLoading(true)
    try { const res = await api.get('/equipment/'); setItems(res.data) }
    catch { message.error('Loi tai du lieu') }
    finally { setLoading(false) }
  }

  useEffect(() => { fetchData() }, [])

  const handleCreate = async (values: any) => {
    try {
      await api.post('/equipment/', {
        ...values,
        last_calibration_date: values.last_calibration_date?.format('YYYY-MM-DD'),
        next_calibration_date: values.next_calibration_date?.format('YYYY-MM-DD'),
      })
      message.success('Them thiet bi thanh cong')
      setModalOpen(false); form.resetFields(); fetchData()
    } catch (err: any) { message.error(err.response?.data?.detail || 'Loi') }
  }

  const handleCalibrate = async (values: any) => {
    if (!calModal) return
    try {
      await api.put(`/equipment/${calModal.id}/calibrate`, null, {
        params: { calibration_date: values.calibration_date.format('YYYY-MM-DD') },
      })
      message.success('Hieu chuan thanh cong')
      setCalModal(null); calForm.resetFields(); fetchData()
    } catch (err: any) { message.error(err.response?.data?.detail || 'Loi') }
  }

  const handleDelete = async (id: number) => {
    await api.delete(`/equipment/${id}`)
    message.success('Xoa thiet bi thanh cong')
    fetchData()
  }

  const columns = [
    { title: 'Ma TB', dataIndex: 'code', key: 'code', width: 100 },
    { title: 'Ten thiet bi', dataIndex: 'name', key: 'name' },
    { title: 'Loai', dataIndex: 'type', key: 'type', width: 100, render: (v: string) => v === 'measurement' ? 'Do luong' : v },
    { title: 'So serie', dataIndex: 'serial_no', key: 'serial', width: 120 },
    { title: 'Vi tri', dataIndex: 'location', key: 'loc' },
    { title: 'Chu ky hieu chuan', key: 'interval', width: 100, render: (_: any, r: Equipment) => `${r.calibration_interval_days} ngay` },
    { title: 'Hieu chuan lan cuoi', key: 'last', width: 120, render: (_: any, r: Equipment) => r.last_calibration_date ? dayjs(r.last_calibration_date).format('DD/MM/YYYY') : '-' },
    {
      title: 'Han hieu chuan', key: 'next', width: 150,
      render: (_: any, r: Equipment) => {
        if (!r.next_calibration_date) return '-'
        return (
          <Tag color={r.calibration_overdue ? 'red' : r.days_until_calibration !== null && r.days_until_calibration <= 30 ? 'orange' : 'green'}>
            {dayjs(r.next_calibration_date).format('DD/MM/YYYY')}
            {r.days_until_calibration !== null && ` (${r.calibration_overdue ? 'Qua han ' + Math.abs(r.days_until_calibration) + ' ngay' : 'Con ' + r.days_until_calibration + ' ngay'})`}
          </Tag>
        )
      },
    },
    {
      title: 'Thao tac', key: 'actions', width: 180,
      render: (_: any, r: Equipment) => (
        <Space>
          <Button size="small" icon={<ToolOutlined />} onClick={() => { setCalModal(r); calForm.setFieldsValue({ calibration_date: dayjs() }) }}>
            Hieu chuan
          </Button>
          <Popconfirm title="Xoa thiet bi nay?" onConfirm={() => handleDelete(r.id)}>
            <Button size="small" danger icon={<DeleteOutlined />} />
          </Popconfirm>
        </Space>
      ),
    },
  ]

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Quan ly thiet bi do & Hieu chuan</h2>
      <Card>
        <div className="flex justify-end mb-4">
          <Button type="primary" icon={<PlusOutlined />} onClick={() => { form.resetFields(); setModalOpen(true) }}>
            Them thiet bi
          </Button>
        </div>
        <Table dataSource={items} columns={columns} rowKey="id" loading={loading} size="middle" />

        <Modal title="Them thiet bi do" open={modalOpen} onCancel={() => setModalOpen(false)} footer={null} width={500}>
          <Form form={form} layout="vertical" onFinish={handleCreate}>
            <Form.Item name="code" label="Ma thiet bi" rules={[{ required: true }]}><Input /></Form.Item>
            <Form.Item name="name" label="Ten thiet bi" rules={[{ required: true }]}><Input /></Form.Item>
            <Form.Item name="type" label="Loai" initialValue="measurement">
              <Select options={[
                { label: 'Thiet bi do luong', value: 'measurement' },
                { label: 'Thiet bi thu nghiem', value: 'testing' },
                { label: 'Dung cu kiem', value: 'gauge' },
                { label: 'Khac', value: 'other' },
              ]} />
            </Form.Item>
            <Form.Item name="serial_no" label="So serie"><Input /></Form.Item>
            <Form.Item name="location" label="Vi tri"><Input /></Form.Item>
            <Form.Item name="calibration_interval_days" label="Chu ky hieu chuan (ngay)" initialValue={365}>
              <InputNumber min={1} className="w-full" />
            </Form.Item>
            <Form.Item name="last_calibration_date" label="Ngay hieu chuan gan nhat"><DatePicker className="w-full" /></Form.Item>
            <Form.Item name="notes" label="Ghi chu"><Input.TextArea rows={2} /></Form.Item>
            <Button type="primary" htmlType="submit" block>Them moi</Button>
          </Form>
        </Modal>

        <Modal title="Hieu chuan thiet bi" open={!!calModal} onCancel={() => setCalModal(null)} footer={null}>
          <p className="mb-3">Dang hieu chuan: <strong>{calModal?.code} - {calModal?.name}</strong></p>
          <Form form={calForm} layout="vertical" onFinish={handleCalibrate}>
            <Form.Item name="calibration_date" label="Ngay hieu chuan" rules={[{ required: true }]}>
              <DatePicker className="w-full" />
            </Form.Item>
            <Button type="primary" htmlType="submit" block>Xac nhan hieu chuan</Button>
          </Form>
        </Modal>
      </Card>
    </div>
  )
}
