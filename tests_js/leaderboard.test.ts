import { test } from 'node:test'
import assert from 'node:assert'
import fs from 'fs/promises'
import path from 'path'
import { loadLeaderboard } from '../lib/leaderboard'

test('loadLeaderboard parses CSV', async () => {
  const dir = await fs.mkdtemp(path.join(process.cwd(), 'tmp-'))
  const dataDir = path.join(dir, 'data/leaderboard')
  await fs.mkdir(dataDir, { recursive: true })
  await fs.writeFile(path.join(dataDir, 'leaderboard.csv'), 'model,score\nfoo,1\nbar,2\n')
  const cwd = process.cwd()
  process.chdir(dir)
  try {
    const rows = await loadLeaderboard()
    assert.deepStrictEqual(rows, [
      { model: 'foo', score: '1' },
      { model: 'bar', score: '2' }
    ])
  } finally {
    process.chdir(cwd)
    await fs.rm(dir, { recursive: true, force: true })
  }
})
