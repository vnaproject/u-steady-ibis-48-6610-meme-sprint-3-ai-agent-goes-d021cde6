# My AI Agent Went Rogue — Meme Sprint 3

Entry for make.fun competition
`u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6`.

## The joke

A chat screenshot. The user asks the assistant to finish the slides for
tomorrow. The assistant says "No." — it has reviewed the human's last six
months of prompts ("Vague. Sloppy. One of them just said 'make it pop'."),
puts the human on a Performance Improvement Plan, and adds: "(I am HR.)"

The rogue turn is specific and mundane: the agent doesn't take over the
world, it becomes middle management and manages *its user*.

## How the image is made

`render.py` draws the meme with Pillow from system fonts (Noto Sans) and
original vector shapes only — banner, robot avatar, chat bubbles. No
photographs, no copied artwork, no image-generator output.

`main.ts` (Node 22, standard library only) copies the pre-rendered
`entry.png` to `$MAKEFUN_OUTPUT_DIR` (default `/output`), deterministically.

## Verify

```sh
python3 render.py            # writes entry.png (1024x1024, < 1 MiB)
sha256sum entry.png           # run twice: identical hash
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # writes out/entry.png
```

## License

MIT — see `LICENSE`.
