'use client'

import { Row } from '@/lib/leaderboard'
import { Chart } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  registerables,
  type ChartDataset,
  type ChartData,
  type ChartOptions,
} from 'chart.js'

ChartJS.register(...registerables)

interface Props {
  rows: Row[]
}

export default function OverallBarChart({ rows }: Props) {
  if (!rows.length) return null
  const labels = ['Overall']
  const colors = ['#4dc9f6', '#f67019', '#f53794', '#537bc4', '#acc236']

  const datasets: ChartDataset<'bar' | 'line', number[]>[] = rows.map((row, idx) => {
    const dataset: ChartDataset<'bar', number[]> = {
      label: row.model_name || row.model,
      data: [Number(row.overall)],
      backgroundColor: colors[idx % colors.length],
      borderColor: 'black',
      borderWidth: 2,
    }
    return dataset
  })

  datasets.push({
    label: 'Human CEO',
    type: 'line',
    data: [100],
    borderColor: '#888',
    borderDash: [4, 4],
    borderWidth: 2,
    pointRadius: 0,
  } as ChartDataset<'line', number[]>)

  const data: ChartData<'bar' | 'line', number[], string> = { labels, datasets }

  const options: ChartOptions<'bar' | 'line'> = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: { mode: 'index' as const, intersect: false },
    plugins: {
      legend: { position: 'top' as const },
    },
    scales: {
      y: { beginAtZero: true },
    },
  }

  return (
    <div className="min-h-[300px]">
      <Chart type='bar' data={data} options={options} />
    </div>
  )
}

