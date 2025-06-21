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
  const ordered = [...rows].sort((a, b) => Number(b.overall) - Number(a.overall))
  const labels = ['Overall']
  const colors = [
    '#4dc9f6',
    '#f67019',
    '#f53794',
    '#537bc4',
    '#acc236',
    '#166a8f',
    '#00a950',
    '#58595b',
    '#8549ba',
    '#b50808',
  ]

  const datasets: ChartDataset<'bar' | 'line', number[]>[] = ordered.map((row, idx) => {
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
    data: [100],
    backgroundColor: colors[datasets.length % colors.length],
    borderColor: 'black',
    borderWidth: 2,
  } as ChartDataset<'bar', number[]>)

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

