'use client'

import { Row } from '@/lib/leaderboard'
import { Chart } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  registerables,
  type ScriptableContext,
  type ChartDataset,
  type ChartData,
  type ChartOptions,
} from 'chart.js'

ChartJS.register(...registerables)

interface Props {
  rows: Row[]
}

export default function ModelsBarChart({ rows }: Props) {
  if (!rows.length) return null
  const topics = Object.keys(rows[0]).filter(k => !['model','model_name','overall','n'].includes(k))
  const labels = ['Overall', ...topics]

  const datasets: ChartDataset<'bar' | 'line', number[]>[] = rows.map((row, idx) => {
    const dataset: ChartDataset<'bar', number[]> = {
      label: row.model_name || row.model,
      data: [Number(row.overall), ...topics.map(t => Number(row[t]))],
      backgroundColor: `var(--color-chart-${(idx % 5) + 1})`,
      borderColor: 'black',
      borderWidth: (ctx: ScriptableContext<'bar'>) =>
        ctx.dataIndex === 0 ? 2 : 0,
    }
    return dataset
  })

  datasets.push({
    label: 'Human CEO',
    type: 'line',
    data: new Array(labels.length).fill(100),
    borderColor: '#888',
    borderDash: [4, 4],
    borderWidth: 2,
    pointRadius: 0,
  } as ChartDataset<'line', number[]>)

  const data: ChartData<'bar' | 'line', number[], string> = { labels, datasets }

  const options: ChartOptions<'bar' | 'line'> = {
    responsive: true,
    interaction: { mode: 'index' as const, intersect: false },
    plugins: {
      legend: { position: 'top' as const },
    },
    scales: {
      y: { beginAtZero: true },
    },
  }

  return <Chart type='bar' data={data} options={options} />
}

