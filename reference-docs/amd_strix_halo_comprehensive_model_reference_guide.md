# AMD Ryzen AI Max+ 395 (128GB Unified Memory) - Comprehensive Model Guide

This guide details every model currently present across your local environment nodes (`amd-halo`, `RyDyn`, and `GeForce`), categorized by architecture, optimal speed, context size, and specific use case on Strix Halo's 256 GB/s memory bandwidth.

---

## 1. High-Performance Coding & Vibe Coding Models

| Model Name | Node / Source | Est. Speed (tok/s) | Optimal Context Size | Best At |
| :--- | :--- | :--- | :--- | :--- |
| **`unsloth/qwen3-coder-next`** | `amd-halo` (Local) | 50–65 tok/s | 32k – 64k | **Primary Backend Agent.** Low active parameters (`512x2.5B`) make it exceptionally fast for multi-file editing, terminal tool loops, and Cline/Continue workflows. |
| **`qwen3.6-35b-a3b`** | `amd-halo` (Local) | 55–70 tok/s | 32k – 64k | **Zero-Quantization-Loss Coding & Vision.** Running at `Q8_0` with native multimodal vision support for analyzing UI screenshots instantly. |
| **`glm-4.7-flash`** | `amd-halo` (Local) | 65–75 tok/s | 32k | **Frontend & UI Layouts.** Exceptional at one-shot React, Tailwind CSS, component scaffolding, and aesthetic UI design. |
| **`qwen3-coder-30b-a3b-instruct`** | `amd-halo` (Local) | 55–70 tok/s | 32k | **Fast Daily Driver.** Reliable mid-size coding assistant with strong multi-language support. |

---

## 2. Architecture, Documentation & Deep Reasoners

| Model Name | Node / Source | Est. Speed (tok/s) | Optimal Context Size | Best At |
| :--- | :--- | :--- | :--- | :--- |
| **`qwen3.5-122b-a10b`** | `amd-halo` (Local) | 25–35 tok/s | 32k – 64k | **Codebase-to-Docs & Refactoring.** High active parameter count yields deep technical comprehension for writing runbooks, ADRs, and complex architecture specs. |
| **`gpt-oss-120b`** | `amd-halo` (Lemonade) | 35–45 tok/s | 32k – 64k | **Structured RFCs & Template Adherence.** Lemonade-optimized build with strict formatting control; behaves like GPT-4o when mapping output to Markdown/Confluence templates. |
| **`nvidia/nemotron-3-super`** | `amd-halo` (Local) | 15–25 tok/s | 32k | **Deep Logic & Complex Debugging.** Heavy reasoning MoE; best deployed in "Architect/Plan" mode rather than raw agentic loops. |
| **`google/gemma-4-31b-qat`** | `amd-halo` (Local) | 12–16 tok/s | 64k – 94k | **Polished Prose & Technical Writing.** Human-like tone with minimal "LLM filler"; ideal for human-facing documentation, executive summaries, and tutorials. |
| **`google/gemma-4-26b-a4b-qat`** | `amd-halo` (Local) | 40–50 tok/s | 64k – 94k | **Balanced Technical Writing & Summaries.** Faster alternative to the 31B model with high prose quality and native QAT precision. |

---

## 3. Specialized, Vision & Utility Models

| Model Name | Node / Source | Est. Speed (tok/s) | Optimal Context Size | Best At |
| :--- | :--- | :--- | :--- | :--- |
| **`nvidia/nemotron-3-nano-omni`** | `amd-halo` (Local) | 40–50 tok/s | 32k | **Omnimodal & Watchdog Support.** Balanced mid-size model for multi-modal tasks and general reasoning support. |
| **`meta/muse-glimmer`** | `amd-halo` (Local) | 25–30 tok/s | 32k | **Creative & Exploratory Generation.** Strong narrative and design generation variant. |
| **`qwen3.8-27b`** | `amd-halo` (Local) | 15–20 tok/s | 64k – 94k | **Visual Diagramming & Mermaid.js.** Converts UI wireframes or architecture diagrams into markdown and Mermaid code. |
| **`qwen3-1.7b`** | `amd-halo` (Local) | 100+ tok/s | 16k | **Speculative Decoding Draft Runner.** Pair as a draft model alongside larger Qwen models inside LM Studio to boost generation speeds by 30%–50%. |
| **`text-embedding-nomic-embed-text-v1.5`** | All Nodes | N/A | 8k | **Local Vector Embeddings.** Powers local RAG search, codebase indexing, and semantic similarity search across all devices. |

---

## 4. Uncensored & Experimental Variants

| Model Name | Node / Source | Est. Speed (tok/s) | Optimal Context Size | Best At |
| :--- | :--- | :--- | :--- | :--- |
| **`qwen3.6-35b-a3b-uncensored-hauhaucs-aggressive`** | `amd-halo` (Local) | 50–60 tok/s | 32k | **Aggressively Abliterated Chat.** Strips all refusal vectors for unfiltered creative or raw conversational logic (use with caution for strict tool-calling). |
| **`qwen3.8-27b-uncensored-hauhaucs-aggressive-mtp`** | `amd-halo` (Local) | 25–35 tok/s | 32k – 64k | **Multi-Token Prediction Uncensored.** Faster multi-token token generation on dense uncensored contexts. |
| **`gemma-4-12b-heretic-abliterated`** | `RyDyn` (Local) | 60–75 tok/s | 32k | **Lightweight Local Uncensored Companion.** Fast edge-device model running locally on Windows desktop. |

---

## Recommended Strix Halo Hardware & Runtime Settings

1. **Flash Attention:** Always enabled in model settings to maximize RDNA 3.5 throughput.
2. **KV Cache Quantization:** Set to `Q8_0` to preserve memory bandwidth during long-context sessions (16k–64k+ tokens).
3. **Prompt Ingestion Batch Size (`ubatch`):** Set to `2048` or `4096` to speed up repo-wide context reading.