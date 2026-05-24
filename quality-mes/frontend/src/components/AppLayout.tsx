import { useState } from 'react'
import { useNavigate, useLocation, Outlet } from 'react-router-dom'
import { Layout, Menu, Button, Avatar, Dropdown, theme, Modal, Form, Input, message } from 'antd'
import {
  DashboardOutlined,
  CheckCircleOutlined,
  ExperimentOutlined,
  WarningOutlined,
  BarChartOutlined,
  LogoutOutlined,
  UserOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  ToolOutlined,
  HistoryOutlined,
  KeyOutlined,
} from '@ant-design/icons'
import { useAuth } from '../contexts/AuthContext'
import api from '../services/api'

const { Header, Sider, Content } = Layout

export default function AppLayout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [collapsed, setCollapsed] = useState(false)
  const [pwdModal, setPwdModal] = useState(false)
  const [pwdForm] = Form.useForm()
  const { token: themeToken } = theme.useToken()

  const menuItems = [
    { key: '/', icon: <DashboardOutlined />, label: 'Bang dieu khien' },
    { key: '/iqc', icon: <CheckCircleOutlined />, label: 'Kiem tra dau vao (IQC)' },
    { key: '/ipqc', icon: <ExperimentOutlined />, label: 'Kiem tra qua trinh (IPQC)' },
    { key: '/oqc', icon: <CheckCircleOutlined />, label: 'Kiem tra thanh pham (OQC)' },
    { key: '/ncr', icon: <WarningOutlined />, label: 'NCR + CAPA' },
    { key: '/equipment', icon: <ToolOutlined />, label: 'Thiet bi do' },
    { key: '/spc', icon: <BarChartOutlined />, label: 'Bao cao (SPC)' },
    { key: '/activity', icon: <HistoryOutlined />, label: 'Nhat ky' },
    { key: '/users', icon: <UserOutlined />, label: 'Nguoi dung' },
  ]

  const userMenuItems = [
    { key: 'password', icon: <KeyOutlined />, label: 'Doi mat khau' },
    { key: 'logout', icon: <LogoutOutlined />, label: 'Dang xuat', danger: true },
  ]

  const handleUserMenuClick = ({ key }: { key: string }) => {
    if (key === 'logout') logout()
    if (key === 'password') { pwdForm.resetFields(); setPwdModal(true) }
  }

  const handleChangePassword = async (values: { old_password: string; new_password: string }) => {
    try {
      await api.post('/change-password', null, { params: values })
      message.success('Doi mat khau thanh cong!')
      setPwdModal(false)
    } catch (err: any) { message.error(err.response?.data?.detail || 'Loi') }
  }

  return (
    <Layout className="min-h-screen">
      <Sider
        trigger={null}
        collapsible
        collapsed={collapsed}
        breakpoint="lg"
        style={{ background: themeToken.colorBgContainer }}
      >
        <div className="h-16 flex items-center justify-center border-b border-gray-100">
          <h1 className="text-lg font-bold text-blue-600 whitespace-nowrap overflow-hidden">
            {collapsed ? 'QM' : 'Quality MES'}
          </h1>
        </div>
        <Menu
          mode="inline"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={({ key }) => navigate(key)}
          style={{ borderInlineEnd: 'none' }}
        />
      </Sider>
      <Layout>
        <Header
          className="flex items-center justify-between px-4"
          style={{ background: themeToken.colorBgContainer, borderBottom: '1px solid #f0f0f0' }}
        >
          <Button
            type="text"
            icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
            onClick={() => setCollapsed(!collapsed)}
          />
          <Dropdown menu={{ items: userMenuItems, onClick: handleUserMenuClick }}>
            <div className="flex items-center gap-2 cursor-pointer">
              <Avatar icon={<UserOutlined />} style={{ background: '#1677ff' }} />
              <span>{user?.full_name}</span>
            </div>
          </Dropdown>
        </Header>
        <Content className="m-6 p-6 bg-white rounded-lg" style={{ minHeight: 360 }}>
          <Outlet />
        </Content>
      </Layout>

      <Modal title="Doi mat khau" open={pwdModal} onCancel={() => setPwdModal(false)} footer={null}>
        <Form form={pwdForm} layout="vertical" onFinish={handleChangePassword}>
          <Form.Item name="old_password" label="Mat khau cu" rules={[{ required: true }]}>
            <Input.Password />
          </Form.Item>
          <Form.Item name="new_password" label="Mat khau moi" rules={[{ required: true, min: 6, message: 'Toi thieu 6 ky tu' }]}>
            <Input.Password />
          </Form.Item>
          <Button type="primary" htmlType="submit" block>Doi mat khau</Button>
        </Form>
      </Modal>
    </Layout>
  )
}
