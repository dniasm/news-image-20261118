// make.fun news-image-20261118 entry: the world's news of Wednesday 18 November 2026 as one front page.
// The picture is drawn ahead of time by draw.py (Pillow) into entry.png; this program only copies it,
// since the grader runs with no network and nothing installed.
//
// Locally: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const png = readFileSync(new URL('./entry.png', import.meta.url));

// Fail loudly rather than hand the gate a file it would reject: a PNG of at most 1 MiB and 1024 x 1024.
const PNG_MAGIC = '89504e470d0a1a0a';
if (png.subarray(0, 8).toString('hex') !== PNG_MAGIC) throw new Error('entry.png is not a PNG');
if (png.length > 1048576) throw new Error(`entry.png is ${png.length} bytes, over 1 MiB`);
const width = png.readUInt32BE(16), height = png.readUInt32BE(20);
if (width > 1024 || height > 1024) throw new Error(`entry.png is ${width}x${height}, over 1024x1024`);

writeFileSync(join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'), png);
