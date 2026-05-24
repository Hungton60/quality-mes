import { useEffect, useState } from 'react'
import { Table, Card, Select, Tag } from 'antd'
import api from '../services/api'
import dayjs from 'dayjs'

interface LogItem {
  id: number; user_id: number | null; username: string; action: string
  module: string; description: string; created_at: string
}

const moduleLabels: Record<string, string> = {
  iqc: 'IQC', oqc: 'OQC', ipqc: 'IPQC', ncr: 'NCR', capa: 'CAPA',
  equipment: 'Thiet bi', user: 'Nguoi dung', auth: 'Dang nhap',
}

const actionColors: Record<string, string> = {
  create: 'green', update: 'blue', delete: 'red', calibrate: 'orange', login: 'purple',
}

export default function ActivityLogPage() {
  const [logs, setLogs] = useState<LogItem[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(false)
  const [module, setModule] = useState<string | undefined>()
  const [page, setPage] = useState(1)

  const fetchLogs = async () => {
    setLoading(true)
    try {
      const params: any = { page, page_size: 50 }
      if (module) params.module = module
      const res = await api.get('/activity-logs', { params })
      setLogs(res.data.items)
      setTotal(res.data.total)
    } catch { /* ignore */ }
    finally { setLoading(false) }
  }

  useEffect(() => { fetchLogs() }, [module, page])

  const columns = [
    { title: 'Thoi gian', key: 'time', width: 160, render: (_: any, r: LogItem) => dayjs(r.created_at).format('DD/MM/YYYY HH:mm:ss') },
    { title: 'Nguoi dung', dataIndex: 'username', key: 'user', width: 150 },
    {
      title: 'Hanh dong', key: 'action', width: 100,
      render: (_: any, r: LogItem) => <Tag color={actionColors[r.action] || 'default'}>{r.action.toUpperCase()}</Tag>,
    },
    {
      title: 'Module', key: 'module', width: 100,
      render: (_: any, r: LogItem) => <Tag>{moduleLabels[r.module] || r.module.toUpperCase()}</Tag>,
    },
    { title: 'Mo ta', dataIndex: 'description', key: 'desc' },
  ]

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Nhat ky hoat dong</h2>
      <Card>
        <div className="mb-4">
          <Select
            allowClear placeholder="Loc theo module" style={{ width: 200 }}
            value={module} onChange={setModule}
            options={Object.entries(moduleLabels).map(([k, v]) => ({ label: v, value: k }))}
          />
        </div>
        <Table
          dataSource={logs} columns={columns} rowKey="id" loading={loading} size="middle"
          pagination={{ current: page, pageSize: 50, total, onChange: setPage }}
        />
      </Card>
    </div>
  )
}
