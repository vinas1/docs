# Cline Settings — Local Gemma 4 via LM Studio

All settings below verified against Cline's official docs unless marked otherwise.

## 1. Provider Setup

| Setting | Value |
|---|---|
| API Provider | LM Studio |
| Base URL | `http://127.0.0.1:1234` (or your DNS helper target, e.g. `llm.devplat.internal:1234`) |
| Model | Select loaded Gemma 4 model from dropdown |

LM Studio works via its OpenAI-compatible server, same setup pattern as Ollama.  

## 2. Features — Required Flags

These settings shown directly impact how local models handle tool calls and file edits.

Here is how each setting affects **Gemma 4 26B A4B QAT** and how to configure them for local execution:

**1. Auto Compact Strategy**

* **Current Setting:** `Agentic`
* **Recommended Change:** Set to **`Truncate`** (or **`Standard`**).
* **Why:** The `Agentic` strategy uses the LLM itself to summarize and rewrite past context. Open-source local models frequently drop system prompts, tool schemas, or strict XML instructions during agentic summaries. `Truncate` simply drops older context items cleanly, preserving system instructions.

**2. Auto Compact**

* **Current Setting:** `Enabled (On)`
* **Recommended Setting:** **`Disabled (Off)`** (or leave enabled if strictly using `Truncate`).
* **Why:** Compacting context causes local models to lose track of tool formatting rules in long sessions. With a 32k context window and 8k max tokens, you rarely need context compression for typical file editing tasks.



**3. Background Edit**

* **Current Setting:** `Disabled (Off)`
* **Recommended Setting:** **`Enabled (On)`**
* **Why:** When enabled, Cline streams diffs directly to disk via background hooks without relying purely on frontend focus handlers. This helps avoid UI dropouts when local models stream tool responses.

**4. Checkpoints**

* **Current Setting:** `Enabled (On)`
* **Recommended Setting:** **`Enabled (On)`**
* **Why:** Keeps local Git shadow commits active so you can instantly roll back if the model makes unintended edits.

**5. Hooks**

* **Current Setting:** `Enabled (On)`
* **Recommended Setting:** **`Enabled (On)`**
* **Why:** Essential for lifecycle execution and tool interception.

**6. MCP Display Mode**

* **Current Setting:** `Plain Text`
* **Recommended Setting:** **`Plain Text`**
* **Why:** Keeps tool responses lightweight, preventing extra markdown/JSON parsing overhead on local context runs.

---

### Quick Summary Matrix

| Setting | Current | Recommended for Local LLMs | Impact |
| --- | --- | --- | --- |
| **Auto Compact Strategy** | Agentic | **Truncate** | Prevents loss of tool XML formatting rules. |
| **Auto Compact** | On | **Off / Truncate** | Stops context rewrites from breaking tool execution. |
| **Background Edit** | Off | **On** | Ensures file diffs execute reliably in the background. |
| **Checkpoints** | On | **On** | Enables safe 1-click rollbacks. |
| **Hooks** | On | **On** | Keeps extension tool integration functional. |
| **MCP Display Mode** | Plain Text | **Plain Text** | Lowers context overhead for your local SearXNG MCP setup.

 |

## 3. Context Window Handling

- **Auto Compact**: when the conversation nears the model's context limit, Cline
  automatically summarizes history (preserving technical decisions/file changes)
  instead of hard-truncating. Enable this as a backstop.  
- **Manual discipline still matters**: start a new task when context balloons rather
  than letting one task run indefinitely — Cline's own local-model recommendation.  
- **Known gap**: historically, Cline didn't always respect a locally-configured
  context window for Ollama/LM Studio-served models — this was fixed for Ollama in
  v3.17.9+ (PR #3880), but at least one report states LM Studio's context window
  "must be configurable" as of mid-2025.  
  `contextLength` explicitly in LM Studio's load config (see `GEMMA.md`) rather than
  relying on Cline to detect it automatically.

## 4. Plan/Act Mode Behavior (how it actually works internally)

- Mode is a persisted setting; switching modes rebuilds the active session with new
  tool permissions.  
- On Plan→Act with an already-presented plan, Cline auto-sends this exact prompt to
  the model: `"The user approved switching to act mode. Continue with the approved
  plan now."` — this is what should trigger immediate implementation.  
- Cline also injects a `<mode_notice>` into the next user message on every mode
  switch specifically so the model doesn't get confused about which tools are
  currently available.  
- You *can* assign different models to Plan vs. Act (e.g., a stronger model for
  planning, faster one for execution) — not required for a single local Gemma 4
  instance, but available if you add a second local model later.  

## 5. Auto-Approve — Recommended Baseline

Official permission categories:  

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
every safety check listed above, including mode transitions.  

## 6. MCP (if you're wiring in tools beyond Cline's built-ins)

Local (STDIO) server config shape:  

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
this if a local Gemma 4 + MCP round-trip is slow on your hardware.  

## 7. Hardware Reality Check

Cline's own stated RAM tiers for local models:  

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
