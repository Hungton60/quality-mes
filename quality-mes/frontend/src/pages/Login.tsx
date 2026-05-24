import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Form, Input, Button, Card, message, Tabs } from 'antd'
import { UserOutlined, LockOutlined, MailOutlined, IdcardOutlined } from '@ant-design/icons'
import { useAuth } from '../contexts/AuthContext'

export default function LoginPage() {
  const { login, register } = useAuth()
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)

  const handleLogin = async (values: { username: string; password: string }) => {
    setLoading(true)
    try {
      await login(values)
      message.success('Dang nhap thanh cong!')
      navigate('/')
    } catch (err: any) {
      message.error(err.response?.data?.detail || 'Dang nhap that bai')
    } finally {
      setLoading(false)
    }
  }

  const handleRegister = async (values: {
    username: string
    email: string
    password: string
    full_name: string
  }) => {
    setLoading(true)
    try {
      await register({ ...values, role: 'inspector' })
      message.success('Dang ky thanh cong! Vui long dang nhap.')
    } catch (err: any) {
      message.error(err.response?.data?.detail || 'Dang ky that bai')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 to-blue-800 flex items-center justify-center p-4">
      <Card className="w-full max-w-md shadow-2xl" styles={{ body: { padding: 32 } }}>
        <div className="text-center mb-6">
          <h1 className="text-2xl font-bold text-blue-600">Quality MES</h1>
          <p className="text-gray-500 mt-1">He thong quan ly chat luong nha may</p>
        </div>

        <Tabs
          centered
          items={[
            {
              key: 'login',
              label: 'Dang nhap',
              children: (
                <Form layout="vertical" onFinish={handleLogin} size="large">
                  <Form.Item name="username" rules={[{ required: true, message: 'Vui long nhap ten dang nhap' }]}>
                    <Input prefix={<UserOutlined />} placeholder="Ten dang nhap" />
                  </Form.Item>
                  <Form.Item name="password" rules={[{ required: true, message: 'Vui long nhap mat khau' }]}>
                    <Input.Password prefix={<LockOutlined />} placeholder="Mat khau" />
                  </Form.Item>
                  <Form.Item>
                    <Button type="primary" htmlType="submit" loading={loading} block>
                      Dang nhap
                    </Button>
                  </Form.Item>
                </Form>
              ),
            },
            {
              key: 'register',
              label: 'Dang ky',
              children: (
                <Form layout="vertical" onFinish={handleRegister} size="large">
                  <Form.Item name="full_name" rules={[{ required: true, message: 'Vui long nhap ho ten' }]}>
                    <Input prefix={<IdcardOutlined />} placeholder="Ho ten" />
                  </Form.Item>
                  <Form.Item name="email" rules={[{ required: true, type: 'email', message: 'Email khong hop le' }]}>
                    <Input prefix={<MailOutlined />} placeholder="Email" />
                  </Form.Item>
                  <Form.Item name="username" rules={[{ required: true, message: 'Vui long nhap ten dang nhap' }]}>
                    <Input prefix={<UserOutlined />} placeholder="Ten dang nhap" />
                  </Form.Item>
                  <Form.Item name="password" rules={[{ required: true, min: 6, message: 'Mat khau toi thieu 6 ky tu' }]}>
                    <Input.Password prefix={<LockOutlined />} placeholder="Mat khau" />
                  </Form.Item>
                  <Form.Item>
                    <Button type="primary" htmlType="submit" loading={loading} block>
                      Dang ky
                    </Button>
                  </Form.Item>
                </Form>
              ),
            },
          ]}
        />
      </Card>
    </div>
  )
}
