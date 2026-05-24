import { useState } from 'react'
import { Card, Select, InputNumber, Descriptions, Tag } from 'antd'

interface AQLData {
  levels: { label: string; value: string }[]
  sample_size_codes: Record<string, (string | null)[]>
  samples: Record<string, number>
}

export default function AQLHelper({ aqlData }: { aqlData: AQLData | null }) {
  const [level, setLevel] = useState<string>('GII')
  const [lotSize, setLotSize] = useState<number>(0)

  if (!aqlData) return null

  const lotSizeIndex = (() => {
    if (lotSize <= 0) return 0
    const ranges = [2, 8, 15, 25, 50, 90, 150, 280, 500, 1200, 3200, 10000, 35000, 150000, 500000, 1000000]
    for (let i = 0; i < ranges.length; i++) {
      if (lotSize <= ranges[i]) return i + 1
    }
    return ranges.length
  })()

  const codeRow = aqlData.sample_size_codes[level]
  const codeLetter = codeRow ? codeRow[lotSizeIndex] : null
  const sampleSize = codeLetter ? aqlData.samples[codeLetter] : null

  const lotSizeLabels = ['', '2-8', '9-15', '16-25', '26-50', '51-90', '91-150', '151-280', '281-500', '501-1200', '1201-3200', '3201-10000', '10001-35000', '35001-150000', '150001-500000', '500001+']

  return (
    <Card size="small" title="Bang lay mau AQL" className="mb-4">
      <div className="flex gap-4 mb-3">
        <div>
          <label className="block text-sm mb-1">Muc kiem tra</label>
          <Select value={level} onChange={setLevel} style={{ width: 200 }}
            options={aqlData.levels}
          />
        </div>
        <div>
          <label className="block text-sm mb-1">Kich thuoc lo</label>
          <InputNumber value={lotSize} onChange={v => setLotSize(v || 0)} min={0} style={{ width: 150 }} />
        </div>
      </div>
      {lotSize > 0 && (
        <Descriptions size="small" column={3} bordered>
          <Descriptions.Item label="Khoang lo">{lotSizeLabels[lotSizeIndex] || 'Tren 500K'}</Descriptions.Item>
          <Descriptions.Item label="Ma co mau"><Tag color="blue">{codeLetter || 'N/A'}</Tag></Descriptions.Item>
          <Descriptions.Item label="Co mau">{sampleSize ? `${sampleSize} pcs` : 'N/A'}</Descriptions.Item>
        </Descriptions>
      )}
    </Card>
  )
}
