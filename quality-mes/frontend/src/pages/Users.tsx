import { useEffect, useState } from 'react'
import {
  Table, Button, Modal, Form, Input, Space, message, Popconfirm, Card,
  Select, Tag, Switch,
} from 'antd'
import { PlusOutlined, DeleteOutlined, EditOutlined } from '@ant-design/icons'
import { useAuth } from '../contexts/AuthContext'
import api from '../services/api'

interface User {
  id: number; username: string; email: string; full_name: string; role: string
  is_active: boolean; created_at: string
}

const roleLabels: Record<string, string> = {
  admin: 'Quan ly', qc_manager: 'Truong QC', inspector: 'Kiem tra vien', operator: 'Cong nhan',
}
const roleColors: Record<string, string> = {
  admin: 'red', qc_manager: 'blue', inspector: 'green', operator: 'default',
}

export default function UsersPage() {
  const { isAdmin } = useAuth()
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(false)
  const [modalOpen, setModalOpen] = useState(false)
  const [editing, setEditing] = useState<User | null>(null)
  const [form] = Form.useForm()

  const fetchUsers = async () => {
    setLoading(true)
    try {
      const res = await api.get('/users/')
      setUsers(res.data)
    } catch { message.error('Loi tai danh sach nguoi dung') }
    finally { setLoading(false) }
  }

  useEffect(() => { fetchUsers() }, [])

  if (!isAdmin) {
    return <Card><p className="text-red-500">Chi Quan ly (admin) moi co quyen truy cap.</p></Card>
  }

  const handleSave = async (values: any) => {
    try {
      if (editing) {
        await api.put(`/users/${editing.id}?role=${values.role}&is_active=${values.is_active}`)
        message.success('Cap nhat nguoi dung thanh cong')
      } else {
        await api.post('/users/', values)
        message.success('Tao nguoi dung thanh cong')
      }
      setModalOpen(false); form.resetFields(); setEditing(null); fetchUsers()
    } catch (err: any) { message.error(err.response?.data?.detail || 'Loi') }
  }

  const handleDelete = async (id: number) => {
    await api.delete(`/users/${id}`)
    message.success('Xoa nguoi dung thanh cong')
    fetchUsers()
  }

  const openEdit = (record: User) => {
    setEditing(record)
    form.setFieldsValue({ role: record.role, is_active: record.is_active, full_name: record.full_name })
    setModalOpen(true)
  }

  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id', width: 60 },
    { title: 'Ten dang nhap', dataIndex: 'username', key: 'username' },
    { title: 'Ho ten', dataIndex: 'full_name', key: 'full_name' },
    { title: 'Email', dataIndex: 'email', key: 'email' },
    {
      title: 'Vai tro', dataIndex: 'role', key: 'role', width: 130,
      render: (role: string) => <Tag color={roleColors[role]}>{roleLabels[role] || role}</Tag>,
    },
    {
      title: 'Trang thai', dataIndex: 'is_active', key: 'active', width: 100,
      render: (v: boolean) => <Tag color={v ? 'green' : 'red'}>{v ? 'Hoat dong' : 'Vo hieu'}</Tag>,
    },
    {
      title: 'Thao tac', key: 'actions', width: 120,
      render: (_: any, record: User) => (
        <Space>
          <Button size="small" icon={<EditOutlined />} onClick={() => openEdit(record)} />
          <Popconfirm title="Xoa nguoi dung nay?" onConfirm={() => handleDelete(record.id)}>
            <Button size="small" danger icon={<DeleteOutlined />} />
          </Popconfirm>
        </Space>
      ),
    },
  ]

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Quan ly nguoi dung</h2>
      <Card>
        <div className="flex justify-end mb-4">
          <Button type="primary" icon={<PlusOutlined />} onClick={() => { setEditing(null); form.resetFields(); setModalOpen(true) }}>
            Them nguoi dung
          </Button>
        </div>
        <Table dataSource={users} columns={columns} rowKey="id" loading={loading} size="middle" />

        <Modal
          title={editing ? 'Sua nguoi dung' : 'Them nguoi dung moi'}
          open={modalOpen} onCancel={() => setModalOpen(false)} footer={null}
        >
          <Form form={form} layout="vertical" onFinish={handleSave}>
            {!editing && (
              <>
                <Form.Item name="username" label="Ten dang nhap" rules={[{ required: true, min: 3 }]}>
                  <Input />
                </Form.Item>
                <Form.Item name="email" label="Email" rules={[{ required: true, type: 'email' }]}>
                  <Input />
                </Form.Item>
                <Form.Item name="password" label="Mat khau" rules={[{ required: true, min: 6 }]}>
                  <Input.Password />
                </Form.Item>
              </>
            )}
            <Form.Item name="full_name" label="Ho ten" rules={[{ required: true }]}>
              <Input />
            </Form.Item>
            <Form.Item name="role" label="Vai tro" rules={[{ required: true }]}>
              <Select options={Object.entries(roleLabels).map(([k, v]) => ({ label: v, value: k }))} />
            </Form.Item>
            {editing && (
              <Form.Item name="is_active" label="Trang thai hoat dong" valuePropName="checked">
                <Switch />
              </Form.Item>
            )}
            <Button type="primary" htmlType="submit" block>
              {editing ? 'Cap nhat' : 'Tao nguoi dung'}
            </Button>
          </Form>
        </Modal>
      </Card>
    </div>
  )
}
