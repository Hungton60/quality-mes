import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Card, Row, Col, Typography, Statistic, Spin, Alert } from 'antd'
import {
  CheckCircleOutlined,
  WarningOutlined,
  ExperimentOutlined,
  BarChartOutlined,
  UserOutlined,
  ToolOutlined,
  HistoryOutlined,
} from '@ant-design/icons'
import api from '../services/api'

const { Title, Text } = Typography

export default function DashboardPage() {
  const navigate = useNavigate()
  const [stats, setStats] = useState<any>(null)
  const [overdue, setOverdue] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      api.get('/spc/summary'),
      api.get('/overdue'),
    ]).then(([statsRes, overdueRes]) => {
      setStats(statsRes.data)
      setOverdue(overdueRes.data)
    }).catch(() => {}).finally(() => setLoading(false))
  }, [])

  const totalAll = stats
    ? stats.iqc.total + stats.oqc.total + stats.ipqc.total
    : 0
  const passAll = stats
    ? stats.iqc.pass + stats.oqc.pass + stats.ipqc.pass
    : 0
  const failAll = stats
    ? stats.iqc.fail + stats.oqc.fail + stats.ipqc.fail
    : 0
  const passRate = totalAll > 0 ? ((passAll / totalAll) * 100).toFixed(1) : '0'

  const modules = [
    {
      title: 'Kiem tra dau vao (IQC)',
      desc: 'Kiem tra chat luong nguyen vat lieu dau vao',
      icon: <CheckCircleOutlined style={{ fontSize: 40, color: '#1677ff' }} />,
      color: '#e6f4ff',
      path: '/iqc',
      stat: stats?.iqc,
    },
    {
      title: 'Kiem tra qua trinh (IPQC)',
      desc: 'Kiem tra chat luong trong qua trinh san xuat',
      icon: <ExperimentOutlined style={{ fontSize: 40, color: '#52c41a' }} />,
      color: '#f6ffed',
      path: '/ipqc',
      stat: stats?.ipqc,
    },
    {
      title: 'Kiem tra thanh pham (OQC)',
      desc: 'Kiem tra chat luong san pham cuoi cung',
      icon: <CheckCircleOutlined style={{ fontSize: 40, color: '#fa8c16' }} />,
      color: '#fff7e6',
      path: '/oqc',
      stat: stats?.oqc,
    },
    {
      title: 'NCR + CAPA',
      desc: 'Bao cao su khong phu hop va hanh dong khac phuc' + (overdue?.overdue_ncrs > 0 ? ` (${overdue.overdue_ncrs + overdue.overdue_capas} qua han)` : ''),
      icon: <WarningOutlined style={{ fontSize: 40, color: '#ff4d4f' }} />,
      color: '#fff2f0',
      path: '/ncr',
      alert: overdue?.overdue_ncrs > 0 || overdue?.overdue_capas > 0,
    },
    {
      title: 'Thiet bi do & Hieu chuan',
      desc: 'Quan ly thiet bi do luong, lich hieu chuan',
      icon: <ToolOutlined style={{ fontSize: 40, color: '#13c2c2' }} />,
      color: '#e6fffb',
      path: '/equipment',
    },
    {
      title: 'Bao cao thong ke (SPC)',
      desc: 'Bieu do, thong ke kiem soat quy trinh',
      icon: <BarChartOutlined style={{ fontSize: 40, color: '#eb2f96' }} />,
      color: '#fff0f6',
      path: '/spc',
    },
    {
      title: 'Nhat ky hoat dong',
      desc: 'Lich su cac thao tac trong he thong',
      icon: <HistoryOutlined style={{ fontSize: 40, color: '#722ed1' }} />,
      color: '#f9f0ff',
      path: '/activity',
    },
    {
      title: 'Quan ly nguoi dung',
      desc: 'Quan ly tai khoan, phan quyen he thong',
      icon: <UserOutlined style={{ fontSize: 40, color: '#52c41a' }} />,
      color: '#f6ffed',
      path: '/users',
    },
  ]

  if (loading) return <div className="flex justify-center py-20"><Spin size="large" /></div>

  return (
    <div>
      <Title level={3} className="mb-6">Bang dieu khien</Title>

      {overdue && (overdue.overdue_ncrs > 0 || overdue.overdue_capas > 0) && (
        <Alert
          type="warning"
          showIcon
          className="mb-4"
          message={`Canh bao: Co ${overdue.overdue_ncrs} NCR va ${overdue.overdue_capas} CAPA da qua han xu ly!`}
          action={
            <a onClick={() => navigate('/ncr')}>Xem ngay</a>
          }
        />
      )}

      <Row gutter={[16, 16]} className="mb-6">
        <Col xs={12} sm={6}>
          <Card><Statistic title="Tong phieu kiem tra" value={totalAll} /></Card>
        </Col>
        <Col xs={12} sm={6}>
          <Card><Statistic title="Dat" value={passAll} valueStyle={{ color: '#3f8600' }} suffix={`/ ${totalAll}`} /></Card>
        </Col>
        <Col xs={12} sm={6}>
          <Card><Statistic title="Khong dat" value={failAll} valueStyle={{ color: '#cf1322' }} /></Card>
        </Col>
        <Col xs={12} sm={6}>
          <Card><Statistic title="Ty le dat" value={passRate} suffix="%" valueStyle={{ color: '#1677ff' }} /></Card>
        </Col>
      </Row>

      {overdue && (
        <Row gutter={[16, 16]} className="mb-6">
          <Col xs={8} sm={4}>
            <Card><Statistic title="NCR dang mo" value={overdue.open_ncrs} valueStyle={{ color: '#ff4d4f' }} /></Card>
          </Col>
          <Col xs={8} sm={4}>
            <Card><Statistic title="NCR da xu ly" value={overdue.resolved_ncrs} valueStyle={{ color: '#722ed1' }} /></Card>
          </Col>
          <Col xs={8} sm={4}>
            <Card><Statistic title="NCR da dong" value={overdue.closed_ncrs} valueStyle={{ color: '#52c41a' }} /></Card>
          </Col>
          <Col xs={8} sm={4}>
            <Card>
              <Statistic title="NCR qua han" value={overdue.overdue_ncrs} valueStyle={{ color: '#ff4d4f' }} />
            </Card>
          </Col>
          <Col xs={8} sm={4}>
            <Card>
              <Statistic title="CAPA qua han" value={overdue.overdue_capas} valueStyle={{ color: '#ff4d4f' }} />
            </Card>
          </Col>
        </Row>
      )}

      <Row gutter={[16, 16]}>
        {modules.map((mod) => (
          <Col xs={24} sm={12} lg={8} key={mod.title}>
            <Card
              hoverable
              onClick={() => navigate(mod.path)}
              className="h-full cursor-pointer transition-shadow hover:shadow-lg"
              style={{ borderLeft: `4px solid ${mod.icon.props.style?.color || '#1677ff'}`, borderColor: mod.alert ? '#ff4d4f' : undefined }}
            >
              <div className="flex items-start gap-4">
                <div
                  className="flex items-center justify-center rounded-lg"
                  style={{ background: mod.color, width: 72, height: 72 }}
                >
                  {mod.icon}
                </div>
                <div className="flex-1">
                  <Title level={5} className="mb-1">{mod.title}</Title>
                  <Text type="secondary">{mod.desc}</Text>
                  {mod.stat && (
                    <div className="mt-2 flex gap-3">
                      <Text className="text-green-600 font-medium">Dat: {mod.stat.pass}</Text>
                      <Text className="text-red-500 font-medium">Khong dat: {mod.stat.fail}</Text>
                    </div>
                  )}
                  {mod.alert && (
                    <div className="mt-1">
                      <Text className="text-red-500 font-medium text-xs">Co viec qua han!</Text>
                    </div>
                  )}
                </div>
              </div>
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  )
}
