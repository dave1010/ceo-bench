import fs from 'fs/promises'
import path from 'path'

export interface Row {
  [key: string]: string
}

export async function loadLeaderboard(): Promise<Row[]> {
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
