# AMD Ryzen AI Max+ 395 (128GB Unified Memory) - Comprehensive Model Guide

This guide details every model currently present across your local environment nodes (`amd-halo`, `RyDyn`, and `GeForce`), categorized by architecture, optimal speed, context size, and specific use case on Strix Halo's 256 GB/s memory bandwidth.

---

### 1. High-Performance Coding & Vibe Coding Models
*Optimized for rapid iteration, agentic workflows, and high-throughput code generation.*

| Model Name | Node(s) | Speed (tok/s) | Context Size | Primary Use Case |
| :--- | :--- | :--- | :--- | :--- |
| `unsloth/qwen3-coder-next` | amd-halo / Local | 50–65 | 32k – 64k | **Primary Backend Agent.** Low active parameters (512x2.5B). |
| `qwen/qwen3-coder-next` | amd-halo / Local | 45–60 | 32k – 64k | Upstream 80B MoE backend agent alternative. |
| `qwen3.6-35b-a3b` | amd-halo / Local | 55–70 | 32k – 64k | Zero-Quantization-Loss Coding & Vision (Q8_0). |
| `glm-4.7-flash` | amd-halo / Local | 65–75 | 32k – 49k | Frontend & UI Layouts. |
| `qwen3-coder-30b-a3b-instruct` | amd-halo / Local | 55–70 | 32k – 64k | Fast Daily Driver. |
| `qwen/qwen3.5-9b` | GeForce / amd-halo | 60–80 | 32k – 64k | High-speed compact dense coding and generalist reasoning. |

### 2. Architecture, Documentation & Deep Reasoners
*Optimized for complex logic, large codebase analysis, and high-fidelity technical prose.*

| Model Name | Node(s) | Speed (tok/s) | Context Size | Primary Use Case |
| :--- | :--- | :--- | :--- | :--- |
| `qwen3.5-122b-a10b` | amd-halo / Local | 25–35 | 32k – 64k | Codebase-to-Docs & Refactoring. |
| `gpt-oss-120b` | amd-halo / Lemonade | 35–45 | 32k – 64k | Structured RFCs & Template Adherence. |
| `nvidia/nemotron-3-super` | amd-halo / Local | 15–25 | 32k – 64k | Deep Logic & Complex Debugging. |
| `google/gemma-4-31b-qat` | amd-halo / Local | 12–16 | 64k – 94k | Polished Prose & Technical Writing. |
| `google/gemma-4-26b-a4b-qat` | amd-halo / Local | 40–50 | 64k – 94k | Balanced Technical Writing & Summaries. |
| `google/gemma-4-12b-qat` | GeForce / amd-halo | 50–70 | 32k – 64k | Agile general reasoning & balanced technical synthesis. |

### 3. Specialized, Vision & Utility Models
*Optimized for multimodal tasks, diagramming, and system-level utility.*

| Model Name | Node(s) | Speed (tok/s) | Context Size | Primary Use Case |
| :--- | :--- | :--- | :--- | :--- |
| `nvidia/nemotron-3.5-super-vl` | amd-halo / Local | 20–30 | 32k – 64k | Heavy multimodal MoE for complex UI, architecture diagrams, and visual code reasoning. |
| `nvidia/nemotron-3-nano-omni` | amd-halo / Local | 40–50 | 32k – 49k | Omnimodal & Watchdog Support. |
| `meta/muse-glimmer` | amd-halo / Local | 25–30 | 32k – 49k | Creative & Exploratory Generation. |
| `qwen3.8-27b` | amd-halo / Local | 15–20 | 64k – 94k | Visual Diagramming & Mermaid.js. |
| `qwen3-1.7b` | amd-halo / Local | 100+ | 16k – 32k | Speculative Decoding Draft Runner. |
| `text-embedding-nomic-embed-text-v1.5` | All Nodes | N/A | 2k | Local Vector Embeddings. |

### 4. Uncensored & Experimental Variants
*Optimized for unrestricted creative exploration and advanced predictive sampling.*

| Model Name | Node(s) | Speed (tok/s) | Context Size | Primary Use Case |
| :--- | :--- | :--- | :--- | :--- |
| `qwen3.6-35b-a3b-uncensored-hauhaucs-aggressive` | amd-halo / Local | 50–60 | 32k – 64k | Aggressively Abliterated Chat. |
| `qwen3.8-27b-uncensored-hauhaucs-aggressive-mtp` | amd-halo / Local | 25–35 | 32k – 64k | Multi-Token Prediction Uncensored. |

---

### 5. Recommended Strix Halo Hardware & Runtime Settings
To maintain the performance metrics listed above, ensure the following runtime configurations are active:

*   **Attention Mechanism:** Flash Attention enabled.
*   **KV Cache Quantization:** `Q8_0` recommended for optimal balance of memory footprint and precision.
*   **Prompt Ingestion:** Set Prompt Ingestion Batch Size (`ubatch`) to `2048` or `4096` to maximize the 256 GB/s bandwidth during prefill stages.