# Local LLM Settings — Cline + LM Studio + Gemma 4

Reference configuration for running **Gemma 4 (12B QAT and larger)** as a local coding
agent backend for **Cline** in VS Code, served via **LM Studio**.

## Folder contents

| File | Covers |
|---|---|
| [`CLINE.md`](./CLINE.md) | Cline (VS Code extension) settings: provider setup, Features flags, Auto-Approve, MCP, Plan/Act behavior |
| [`GEMMA.md`](./GEMMA.md) | LM Studio-side settings for Gemma 4: model variants, load parameters, sampling defaults, known bugs/fixes |
| [`.clinerules/`](../.clinerules/) | Modular agent-behavior rules (separate from this folder — see repo root) |

## Reference hardware (this deployment)

| Machine | Spec | Role |
|---|---|---|
| MacBook Pro M5 | 48GB unified memory | AIRIC LLM workload client |
| Lab box | 16 CPUs, 20GB RAM, headless Debian, RTX 5060 Ti 16GB | LM Studio host (`llm.devplat.internal`) |

QAT VRAM figures in `GEMMA.md` are sized against the 16GB 5060 Ti specifically.

## Verification status

Every setting below is sourced from official Google/Cline/LM Studio documentation
where possible. Anything derived from community benchmarks or third-party guides
instead of vendor docs is explicitly labeled **(community/unverified)** — treat
those as a tuned starting point, not a guarantee.

## Quick start

1. Load a Gemma 4 QAT checkpoint (12B or larger) in LM Studio — see `GEMMA.md` for
   which size fits your GPU and the load parameters to set.
2. Start the LM Studio local server.
3. Point Cline at it — see `CLINE.md` for provider config and the Features flags
   that matter for local models specifically.
4. Drop the `.clinerules/` folder in your repo root for agent behavior guardrails.

## Known open issue to watch

Gemma 4 12B has a documented tool-calling failure pattern in some eval harnesses,
with a community-found fix involving a custom chat template. See the "Known Issues"
section in `GEMMA.md` before assuming a tool-call failure is a Cline bug. <cite>turn5search98</cite>
