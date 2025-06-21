'use client'

import { Row } from '@/lib/leaderboard'
import { Bar } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  type ScriptableContext,
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Tooltip,
  Legend
)

interface Props {
  rows: Row[]
}

export default function ModelsBarChart({ rows }: Props) {
  if (!rows.length) return null
  const topics = Object.keys(rows[0]).filter(k => !['model','model_name','overall','n'].includes(k))
  const labels = ['Overall', ...topics]

  const datasets = rows.map((row, idx) => ({
    label: row.model_name || row.model,
    data: [Number(row.overall), ...topics.map(t => Number(row[t]))],
    backgroundColor: `var(--color-chart-${(idx % 5) + 1})`,
    borderColor: 'black',
    borderWidth: (ctx: ScriptableContext<'bar'>) =>
      ctx.dataIndex === 0 ? 2 : 0,
  }))

  datasets.push({
    label: 'Human CEO',
    type: 'line' as const,
    data: new Array(labels.length).fill(100),
    borderColor: '#888',
    borderDash: [4,4],
    borderWidth: 2,
    pointRadius: 0,
  })

  const data = { labels, datasets }

  const options = {
    responsive: true,
    interaction: { mode: 'index' as const, intersect: false },
    stacked: false,
    plugins: {
      legend: { position: 'top' as const },
    },
    scales: {
      y: { beginAtZero: true },
    },
  }

  return <Bar data={data} options={options} />
}

