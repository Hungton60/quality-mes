import { useEffect, useState } from 'react'
import { Card, Row, Col, Statistic, Spin, Select, Tabs, Tag } from 'antd'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line, Cell } from 'recharts'
import api from '../services/api'

interface Summary {
  iqc: { total: number; pass: number; fail: number }
  oqc: { total: number; pass: number; fail: number }
  ipqc: { total: number; pass: number; fail: number }
}

interface ParetoItem {
  item_name: string; count: number
}

interface ResultRow {
  item_name: string; measured_value: number; standard_min: number | null
  standard_max: number | null; result: string; created_at: string
}

const COLORS = ['#1677ff', '#52c41a', '#fa8c16', '#ff4d4f', '#722ed1', '#13c2c2', '#eb2f96', '#a0d911', '#faad14', '#2f54eb']

export default function SPCPage() {
  const [summary, setSummary] = useState<Summary | null>(null)
  const [paretoIqc, setParetoIqc] = useState<ParetoItem[]>([])
  const [paretoOqc, setParetoOqc] = useState<ParetoItem[]>([])
  const [results, setResults] = useState<ResultRow[]>([])
  const [module, setModule] = useState<string>('iqc')
  const [loading, setLoading] = useState(true)

  const fetchData = async () => {
    setLoading(true)
    try {
      const [sumRes, piqc, poqc] = await Promise.all([
        api.get('/spc/summary'),
        api.get('/spc/pareto/iqc'),
        api.get('/spc/pareto/oqc'),
      ])
      setSummary(sumRes.data)
      setParetoIqc(piqc.data)
      setParetoOqc(poqc.data)
    } catch { /* ignore */ }
    finally { setLoading(false) }
  }

  const fetchResults = async (mod: string) => {
    try {
      const res = await api.get(`/spc/results/${mod}`, { params: { limit: 200 } })
      setResults(res.data)
    } catch { /* ignore */ }
  }

  useEffect(() => { fetchData() }, [])
  useEffect(() => { fetchResults(module) }, [module])

  const passRate = (pass: number, total: number) => total > 0 ? ((pass / total) * 100).toFixed(1) : '0'

  const controlChartData = () => {
    const groups: Record<string, { values: number[]; min: number | null; max: number | null }> = {}
    results.forEach(r => {
      if (!groups[r.item_name]) groups[r.item_name] = { values: [], min: r.standard_min, max: r.standard_max }
      groups[r.item_name].values.push(r.measured_value)
    })
    return Object.entries(groups).map(([name, g]) => ({
      name,
      xbar: g.values.length ? +(g.values.reduce((a, b) => a + b, 0) / g.values.length).toFixed(3) : 0,
      min: g.min,
      max: g.max,
    }))
  }

  const histogramData = () => {
    const values = results.map(r => r.measured_value).sort((a, b) => a - b)
    if (values.length < 2) return []
    const min = Math.floor(values[0])
    const max = Math.ceil(values[values.length - 1])
    const range = max - min
    const binCount = Math.min(10, Math.ceil(Math.sqrt(values.length)))
    const binWidth = range / binCount || 1
    const bins: { range: string; count: number }[] = []
    for (let i = 0; i < binCount; i++) {
      const low = +(min + i * binWidth).toFixed(1)
      const high = +(min + (i + 1) * binWidth).toFixed(1)
      bins.push({ range: `${low}-${high}`, count: 0 })
    }
    values.forEach(v => {
      const idx = Math.min(Math.floor((v - min) / binWidth), binCount - 1)
      if (idx >= 0 && idx < bins.length) bins[idx].count++
    })
    return bins
  }

  if (loading) return <div className="flex justify-center py-20"><Spin size="large" /></div>

  const paretoData = module === 'oqc' ? paretoOqc : paretoIqc

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Bao cao thong ke (SPC)</h2>

      <Row gutter={[16, 16]} className="mb-6">
        {summary && Object.entries(summary).map(([key, val]) => (
          <Col xs={24} sm={8} key={key}>
            <Card>
              <h3 className="text-lg font-semibold mb-3 uppercase">{key}</h3>
              <Row gutter={8}>
                <Col span={8}><Statistic title="Tong" value={val.total} /></Col>
                <Col span={8}><Statistic title="Dat" value={val.pass} valueStyle={{ color: '#3f8600' }} /></Col>
                <Col span={8}><Statistic title="Khong dat" value={val.fail} valueStyle={{ color: '#cf1322' }} /></Col>
              </Row>
              <div className="mt-2 text-center">
                <Tag color="blue">Ty le dat: {passRate(val.pass, val.total)}%</Tag>
              </div>
            </Card>
          </Col>
        ))}
      </Row>

      <Tabs
        items={[
          {
            key: 'charts',
            label: 'Bieu do kiem soat',
            children: (
              <Row gutter={[16, 16]}>
                <Col xs={24} lg={12}>
                  <Card title="X-bar Chart (Trung binh)">
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart data={controlChartData()}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="xbar" fill="#1677ff" name="Gia tri TB" />
                        <Bar dataKey="min" fill="#52c41a" name="Gioi han duoi" />
                        <Bar dataKey="max" fill="#ff4d4f" name="Gioi han tren" />
                      </BarChart>
                    </ResponsiveContainer>
                  </Card>
                </Col>
                <Col xs={24} lg={12}>
                  <Card title="Histogram (Phan bo)">
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart data={histogramData()}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="range" />
                        <YAxis />
                        <Tooltip />
                        <Bar dataKey="count" name="Tan suat">
                          {histogramData().map((_, i) => (
                            <Cell key={i} fill={COLORS[i % COLORS.length]} />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </Card>
                </Col>
              </Row>
            ),
          },
          {
            key: 'pareto',
            label: 'Bieu do Pareto',
            children: (
              <Card title={`Pareto - Loi thuong gap (${module.toUpperCase()})`}>
                <div className="mb-4">
                  <Select value={module} onChange={setModule} style={{ width: 150 }}>
                    <Select.Option value="iqc">IQC</Select.Option>
                    <Select.Option value="oqc">OQC</Select.Option>
                    <Select.Option value="ipqc">IPQC</Select.Option>
                  </Select>
                </div>
                {paretoData.length === 0 ? (
                  <p className="text-gray-400">Chua co du lieu loi.</p>
                ) : (
                  <ResponsiveContainer width="100%" height={400}>
                    <BarChart data={paretoData} layout="vertical">
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis type="number" />
                      <YAxis dataKey="item_name" type="category" width={150} />
                      <Tooltip />
                      <Bar dataKey="count" name="So loi" radius={[0, 4, 4, 0]}>
                        {paretoData.map((_, i) => (
                          <Cell key={i} fill={COLORS[i % COLORS.length]} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                )}
              </Card>
            ),
          },
          {
            key: 'trend',
            label: 'Xu huong theo thoi gian',
            children: (
              <Card title={`Du lieu do luong - ${module.toUpperCase()}`}>
                <div className="mb-4">
                  <Select value={module} onChange={setModule} style={{ width: 150 }}>
                    <Select.Option value="iqc">IQC</Select.Option>
                    <Select.Option value="oqc">OQC</Select.Option>
                    <Select.Option value="ipqc">IPQC</Select.Option>
                  </Select>
                </div>
                {results.length === 0 ? (
                  <p className="text-gray-400">Chua co du lieu.</p>
                ) : (
                  <ResponsiveContainer width="100%" height={400}>
                    <LineChart data={results.map((r, i) => ({ ...r, index: i + 1 }))}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="index" label={{ value: 'Lan do', position: 'insideBottomRight', offset: -5 }} />
                      <YAxis />
                      <Tooltip
                        labelFormatter={(label) => results[Number(label) - 1]?.item_name || `#${label}`}
                        formatter={(value: any) => [Number(value).toFixed(3), 'Gia tri do']}
                      />
                      <Line type="monotone" dataKey="measured_value" stroke="#1677ff" name="Gia tri do" dot={{ r: 2 }} />
                      <Line type="monotone" dataKey="standard_min" stroke="#52c41a" name="LCL" strokeDasharray="5 5" dot={false} />
                      <Line type="monotone" dataKey="standard_max" stroke="#ff4d4f" name="UCL" strokeDasharray="5 5" dot={false} />
                    </LineChart>
                  </ResponsiveContainer>
                )}
              </Card>
            ),
          },
        ]}
      />
    </div>
  )
}
