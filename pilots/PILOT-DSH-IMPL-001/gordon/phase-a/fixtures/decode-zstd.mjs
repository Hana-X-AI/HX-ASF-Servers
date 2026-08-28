// Gordon fixture: decode a .jsonl.zstd session artifact to stdout.
// The backend writes a concatenated-frame container (session-persistence-jsonl
// zstd.ts); Node's streaming decompressor walks the frames in order.
// Usage: node decode-zstd.mjs <artifact>
import { createReadStream } from 'node:fs'
import { createZstdDecompress } from 'node:zlib'
import { pipeline } from 'node:stream/promises'

const file = process.argv[2]
if (!file) {
  process.stderr.write('usage: node decode-zstd.mjs <artifact>\n')
  process.exit(2)
}
await pipeline(createReadStream(file), createZstdDecompress(), process.stdout)
