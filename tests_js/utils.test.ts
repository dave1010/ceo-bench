import { test } from 'node:test'
import assert from 'node:assert'
import { cn } from '../lib/utils'

test('cn combines class names', () => {
  assert.strictEqual(cn('a', 'b'), 'a b')
})
