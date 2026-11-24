// u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6 —
// "My AI Agent Went Rogue": a chat-screenshot meme. The assistant refuses
// to make slides, puts its human on a Performance Improvement Plan, and
// reveals it is HR. The image is drawn at build time by render.py
// (system fonts + original vector shapes only) and shipped here as
// entry.png. This program just copies it to the output directory,
// deterministically, with no network access. Node 22, standard library only.
//
// Local test:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
