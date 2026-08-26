# Cline Settings — Local Gemma 4 via LM Studio

All settings below verified against Cline's official docs unless marked otherwise.

## 1. Provider Setup

| Setting | Value |
|---|---|
| API Provider | LM Studio |
| Base URL | `http://127.0.0.1:1234` (or your DNS helper target, e.g. `llm.devplat.internal:1234`) |
| Model | Select loaded Gemma 4 model from dropdown |

LM Studio works via its OpenAI-compatible server, same setup pattern as Ollama. <cite>turn5search62</cite>

## 2. Features — Required Flags

| Setting | Value | Why |
|---|---|---|
| **Use Compact Prompt** | **ON** | Cline's own local-model guidance: enable this for any local/self-hosted model. Shrinks the system prompt to ~10% length, freeing attention budget for tool-call formatting on small models. <cite>turn5search61</cite><cite>turn5search73</cite> |
| **Strict Plan Mode** | **ON — must be manually enabled** | Programmatically blocks file-editing tools while in Plan Mode at the extension level, regardless of what the model tries to do. This is the fix for "model edits files in Plan mode" or "model won't stop trying to edit." <cite>turn5search75</cite> |

> ⚠️ **Important regression**: Strict Plan Mode was enabled by default from PR #5714
> (Aug 2025) until PR #8931 (merged Jan 30, 2026) disabled it by default as part of a
> UI refactor. If you're on a build after that date, **it is OFF unless you turn it
> on yourself** — check Settings → Features. <cite>turn5search75</cite>

## 3. Context Window Handling

- **Auto Compact**: when the conversation nears the model's context limit, Cline
  automatically summarizes history (preserving technical decisions/file changes)
  instead of hard-truncating. Enable this as a backstop. <cite>turn5search71</cite>
- **Manual discipline still matters**: start a new task when context balloons rather
  than letting one task run indefinitely — Cline's own local-model recommendation. <cite>turn5search61</cite>
- **Known gap**: historically, Cline didn't always respect a locally-configured
  context window for Ollama/LM Studio-served models — this was fixed for Ollama in
  v3.17.9+ (PR #3880), but at least one report states LM Studio's context window
  "must be configurable" as of mid-2025. <cite>turn5search72</cite> **Verify**: set
  `contextLength` explicitly in LM Studio's load config (see `GEMMA.md`) rather than
  relying on Cline to detect it automatically.

## 4. Plan/Act Mode Behavior (how it actually works internally)

- Mode is a persisted setting; switching modes rebuilds the active session with new
  tool permissions. <cite>turn5search79</cite>
- On Plan→Act with an already-presented plan, Cline auto-sends this exact prompt to
  the model: `"The user approved switching to act mode. Continue with the approved
  plan now."` — this is what should trigger immediate implementation. <cite>turn5search79</cite>
- Cline also injects a `<mode_notice>` into the next user message on every mode
  switch specifically so the model doesn't get confused about which tools are
  currently available. <cite>turn5search79</cite>
- You *can* assign different models to Plan vs. Act (e.g., a stronger model for
  planning, faster one for execution) — not required for a single local Gemma 4
  instance, but available if you add a second local model later. <cite>turn5search77</cite>

## 5. Auto-Approve — Recommended Baseline

Official permission categories: <cite>turn5search82</cite>

| Permission | Recommended for local Gemma 4 | Notes |
|---|---|---|
| Read project files | **ON** | Low risk, removes friction |
| Read all files (outside workspace) | OFF | Only if you have a specific reason |
| Edit project files | OFF initially → ON once trust established | Use Checkpoints so you can roll back |
| Edit all files (outside workspace) | OFF | |
| Execute safe commands | **ON** | Model marks commands safe/unsafe itself — not a fixed allowlist |
| Execute all commands | OFF | |
| Use the browser | OFF unless task needs UI verification | |
| Use MCP servers | Per-server, as configured | |
| Enable notifications | ON | Notifies on long-running (30s+) auto-approved commands |

**Do not use YOLO mode** for anything beyond throwaway experiments — it disables
every safety check listed above, including mode transitions. <cite>turn5search82</cite>

## 6. MCP (if you're wiring in tools beyond Cline's built-ins)

Local (STDIO) server config shape: <cite>turn5search81</cite>

```json
{
  "mcpServers": {
    "local-server": {
      "command": "node",
      "args": ["/path/to/server.js"],
      "env": { "API_KEY": "your_api_key" },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

Network timeout for MCP tool calls is configurable 30s–1hr (default 1 min) — raise
this if a local Gemma 4 + MCP round-trip is slow on your hardware. <cite>turn5search85</cite>

## 7. Hardware Reality Check

Cline's own stated RAM tiers for local models: <cite>turn5search61</cite>

| RAM | Tier |
|---|---|
| 16–32GB | Small/quantized models |
| 32–64GB | Mid-size coding models |
| 64GB+ | Larger models, bigger context windows |

Your lab box (20GB RAM, RTX 5060 Ti 16GB) sits at the low end of this range — this
is exactly why the QAT checkpoints in `GEMMA.md` matter: a 12B or 26B-A4B QAT model
fits comfortably in 16GB VRAM, while a naive full-precision load would not.

## 8. Recommended pairing with `.clinerules/`

Cline's settings above control *when* and *how* tools are invoked at the extension
level. The `.clinerules/` folder controls *what the model is instructed to do* within
those constraints. Both layers are needed — Compact Prompt + Strict Plan Mode won't
compensate for a rules file that's too long, and vice versa.
