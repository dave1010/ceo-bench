import fs from 'fs/promises'
import path from 'path'
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { BarChart3, Trophy } from "lucide-react"

interface Row {
  [key: string]: string
}

async function loadCsv(): Promise<Row[]> {
  const csvPath = path.join(process.cwd(), 'data/leaderboard/leaderboard.csv')
  const text = await fs.readFile(csvPath, 'utf8')
  const lines = text.trim().split(/\r?\n/)
  const headers = lines[0].split(',').map(h => h.trim())
  return lines.slice(1).map(line => {
    const values = line.split(',').map(v => v.trim())
    const row: Row = {}
    headers.forEach((h, i) => {
      row[h] = values[i] ?? ''
    })
    return row
  })
}

function format(val?: string) {
  if (!val) return '–'
  const num = Number(val)
  return isNaN(num) ? '–' : num.toFixed(1)
}

export default async function Leaderboard() {
  const rows = await loadCsv()
  const topics = rows[0]
    ? Object.keys(rows[0]).filter(
        k => !['model', 'model_name', 'overall', 'n'].includes(k)
      )
    : []
  const sorted = rows.sort((a, b) => Number(b.overall) - Number(a.overall))

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <BarChart3 className="w-5 h-5" />
          <span>Model Performance Rankings</span>
        </CardTitle>
        <CardDescription>
          Scores represent percentage accuracy across all CEO Bench evaluation tasks
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b">
                <th className="text-left py-3 px-2 font-semibold text-slate-700">Rank</th>
                <th className="text-left py-3 px-2 font-semibold text-slate-700">Model</th>
                <th className="text-center py-3 px-2 font-semibold text-slate-700">Overall</th>
                {topics.map(topic => (
                  <th key={topic} className="text-center py-3 px-2 font-semibold text-slate-700">
                    {topic}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {sorted.map((row, idx) => (
                <tr key={row.model} className="border-b hover:bg-slate-50/50">
                  <td className="py-4 px-2">
                    <div className="flex items-center space-x-2">
                      {idx < 3 && (
                        <Trophy
                          className={`w-4 h-4 ${
                            idx === 0
                              ? 'text-yellow-500'
                              : idx === 1
                                ? 'text-slate-400'
                                : 'text-amber-600'
                          }`}
                        />
                      )}
                      <span className="font-semibold text-slate-900">#{idx + 1}</span>
                    </div>
                  </td>
                  <td className="py-4 px-2">
                    <span className="font-medium text-slate-900">{row.model_name || row.model}</span>
                  </td>
                  <td className="py-4 px-2 text-center">
                    <Badge variant={idx < 3 ? 'default' : 'secondary'} className="font-semibold">
                      {format(row.overall)}
                    </Badge>
                  </td>
                  {topics.map(topic => (
                    <td key={topic} className="py-4 px-2 text-center text-slate-700">
                      {format(row[topic])}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  )
}
