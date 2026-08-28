// Gordon fixture: decode a .jsonl.zstd session artifact to stdout.
// The backend appends CONCATENATED zstd frames per write batch
// (session-persistence-jsonl zstd.ts; Morpheus receipt §9: Node's one-shot /
// streaming decode yields frame 1 only). Decode frame-wise: split on the
// little-endian magic 28 b5 2f fd and decompress each frame.
// Usage: node decode-zstd.mjs <artifact>
import { readFileSync } from 'node:fs'
import { zstdDecompressSync } from 'node:zlib'

const file = process.argv[2]
if (!file) {
  process.stderr.write('usage: node decode-zstd.mjs <artifact>\n')
  process.exit(2)
}

const buf = readFileSync(file)
const MAGIC = Buffer.from([0x28, 0xb5, 0x2f, 0xfd])
const starts = []
let idx = buf.indexOf(MAGIC)
while (idx !== -1) {
  starts.push(idx)
  idx = buf.indexOf(MAGIC, idx + 4)
}
if (starts.length === 0 || starts[0] !== 0) {
  process.stderr.write('decode-zstd: no zstd frame at offset 0\n')
  process.exit(1)
}
const chunks = []
for (let i = 0; i < starts.length; i++) {
  const end = i + 1 < starts.length ? starts[i + 1] : buf.length
  try {
    chunks.push(zstdDecompressSync(buf.subarray(starts[i], end)))
  } catch (error) {
    // A magic byte run inside compressed payload lands here. Fail loud so the
    // caller can fall back to the zstd CLI instead of trusting a partial read.
    process.stderr.write(`decode-zstd: frame ${i} at offset ${starts[i]} failed: ${error.message}\n`)
    process.exit(1)
  }
}
process.stdout.write(Buffer.concat(chunks))
