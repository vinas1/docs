# Gemma 4 Settings — LM Studio

Covers Gemma 4 **12B and larger** (12B, 26B-A4B MoE, 31B dense), with emphasis on the
official **QAT (Quantization-Aware Training)** checkpoints released by Google.

## 1. Model Variants

| Model | Params | Architecture | Native context | Notes |
|---|---|---|---|---|
| E2B / E4B | 2B / 4B | Dense, edge-optimized | 128K | Not covered here — below your "12B and larger" floor |
| **12B** | 12B | Dense, unified (encoder-free) | **256K** | Newest addition to the family (added ~2 months after initial launch) <cite> </cite> |
| **26B-A4B** | 26B total / ~4B active | Mixture-of-Experts | **256K** | High throughput per VRAM dollar |
| **31B** | 31B | Dense | **256K** | Highest quality tier, most VRAM-hungry |

Official Google source for context windows and architecture:  

All Gemma 4 models ship native function-calling support and native system-prompt
support — no special jailbreak or prompt trick needed to get tool-call attempts,
though see the Known Issues section below on reliability.  

## 2. QAT Checkpoints — Use These, Not Naive Q4

Google released official QAT checkpoints on **June 5, 2026** for E2B, E4B, 12B, and
31B (26B-A4B QAT is distributed via Ollama's `-it-qat` GGUF tag rather than the
official w4a16 release). QAT simulates quantization *during* training rather than
compressing after the fact, so a QAT 4-bit checkpoint holds quality much closer to
BF16 than a standard post-training-quantized (PTQ) Q4 of the same size.  

**Approximate VRAM by model, QAT Q4_0:**

| Model | QAT VRAM | Fits your 16GB RTX 5060 Ti? |
|---|---|---|
| 12B | ~7GB | ✅ Comfortably, with headroom for large context |
| 26B-A4B | ~15GB | ✅ Tight but fits |
| 31B | ~18GB | ❌ Needs a 24GB card — will spill to CPU/RAM on 16GB |

Sources: Google's official blog post gives the QAT methodology and confirms the
release scope;  
corroborated across independent QAT summaries and an AMD 7900 XTX benchmark showing
a 5.7GB VRAM reduction for 12B QAT vs. Q8_0.  
**Label: cross-verified across multiple sources, but not a single primary Google
number — treat as accurate to within ~1GB.**

**Practical takeaway for your lab box**: 12B QAT and 26B-A4B QAT both run entirely
on-GPU at 16GB. 31B QAT does not — either accept CPU/RAM offload (slower) or reserve
31B for a machine with 24GB+.

Download: search `-it-qat` GGUF variants on Hugging Face/Ollama library, or use
Unsloth's pre-converted GGUFs — hand-converting the QAT checkpoints yourself risks
losing the quality QAT was meant to preserve.  

## 3. LM Studio Load Parameters (set at model load, requires reload to change)

Official parameter names from LM Studio's API reference:  

| Parameter | Recommended value | Why |
|---|---|---|
| `contextLength` | 32,768 minimum; up to 256K if VRAM allows | Matches your stated 32K floor; Gemma 4 12B+ natively supports up to 256K  
| `flashAttention` | `true` | Reduces memory use, speeds generation on compatible hardware (RTX 5060 Ti supports it)  
| `useFp16ForKVCache` | `true` (or leave KV cache unquantized per Cline's own stack guide) | Cline's official local-stack blog explicitly recommends leaving KV Cache Quantization **unchecked** when pairing with Cline  
| `gpu` (offload ratio) | Max your VRAM allows | Full GPU offload where possible |
| `evalBatchSize` | Default, raise only if VRAM headroom exists | Trades memory for throughput  
| `keepModelInMemory` | `true` if RAM allows | Avoids reload latency between tasks |
| `num_experts` | Default for 26B-A4B (MoE only) | Only applies to the MoE variant  

**Context length reality check**: raising context length increases KV-cache VRAM
roughly linearly. A rough community-sourced guide (not vendor-official) suggests a
16GB card comfortably supports 16–32K context on a 12–14B Q4 model — treat 256K as
theoretically supported by the model architecture but not necessarily practical on
your 16GB card without dropping to CPU offload for the KV cache at very long
contexts.  

## 4. Sampling / Inference Parameters

**Official Gemma 4 defaults**, as shipped in the Ollama model library params.json
for the Gemma 4 family:  

| Parameter | Official default |
|---|---|
| `temperature` | 1.0 |
| `top_k` | 64 |
| `top_p` | 0.95 |

**Coding/agentic-tuned alternative (community, not vendor-official)** — lower
temperature trades creativity for determinism, which generally helps tool-call
reliability and reduces hallucinated file paths/arguments:

| Parameter | Coding-tuned value | Source status |
|---|---|---|
| `temperature` | 0.2–0.3 | Community consensus across multiple independent guides  
| `top_p` | 0.85–0.9 | Same |
| `top_k` | 40 | Same |
| `repeat_penalty` | 1.05–1.1 | Same |

One community benchmark reports the *opposite* finding for Gemma 4 specifically —
higher temperature (~1.2) for coding — attributing it to the model's built-in
reasoning/thinking behavior interacting oddly with low temperature. This directly
conflicts with the general-purpose coding guidance above.  
**Label: conflicting community sources — start with the low-temperature coding
preset (it's the majority recommendation and matches general LLM tool-calling best
practice), and only raise temperature if you observe truncated/repetitive output.**

## 5. Infinite-Generation / Thinking-Loop Mitigation

Gemma-family models documented to enter unbounded thinking loops under long system
prompts (>~10K tokens) with no natural stop condition. Reported mitigation:
`repeat_penalty ≈ 1.08` with `repeat_last_n ≈ 4096`. This reduces but does not
eliminate the failure mode — keeping your `.clinerules` compact (per the Cline-side
doc) is the more durable fix. *(Carried forward from prior verified finding in this
session — GitHub issue tracking `gemma-4-12B-it` on llama.cpp/LM Studio.)*

## 6. Speculative Decoding (built-in, free speed)

Every Gemma 4 model ships a **dedicated draft model for Multi-Token Prediction
(MTP)** as part of its architecture — this is speculative decoding support built in
at the model level, not something you configure separately.  

In LM Studio: switch to **Power User mode**, load your main model, then select a
**Draft Model** in the Speculative Decoding section of the chat sidebar.  
General guidance for draft-model sizing (applies if you pair main 31B with a smaller
Gemma 4 variant as draft, e.g. E4B):  

| Main model size | Max effective draft model size |
|---|---|
| 14B | ~3B |
| 32B | ~7B |

## 7. Known Issues

### Gemma 4 12B tool-calling failures
Documented failures where Gemma 4 12B does not emit valid tool calls in evaluation
harnesses. Community-found fix: compile llama.cpp from source and apply a custom
chat template using `--jinja --chat-template-file` flags. <cite> </cite>

**For LM Studio specifically (label: unverified — LM Studio bundles its own
llama.cpp runtime, GUI equivalent not independently confirmed in this session)**:
check the model's **Prompt Template** tab under Advanced Configuration before
loading — if tool calls are silently failing or narrating instead of executing,
compare the active template against the model's documented chat template and
override it manually if they don't match.

### Reasoning/thinking trace intercepting tool calls
Gemma 4's configurable thinking mode can route tool-call output to a
`reasoning_content` field instead of `content` unless thinking is explicitly
disabled for the load — meaning the tool call never reaches Cline's parser. Disable
thinking/reasoning mode for this model when using it as a Cline backend. *(Carried
forward from prior verified finding in this session.)*

## 8. Structured Output (optional, for non-Cline scripting)

LM Studio supports rigorously enforcing output structure via JSON schema or Zod
schema on the inference-time `structured` config field — useful if you're scripting
against Gemma 4 outside of Cline (e.g., a custom AIRIC reviewer call) and want
guaranteed-parseable output rather than relying on prompt instructions alone.  
