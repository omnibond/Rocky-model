# Project Hail Mary: Rocky AI 🪨🎶

This repository contains a full pipeline to fine-tune the highly intelligent **Qwen2.5** (7B foundational and 1.5B lightweight edge) Large Language Models specifically into **Rocky**, the beloved Eridian engineer from Andy Weir's *Project Hail Mary*. 

Operating entirely on Apple Silicon's **MLX** neural net optimization, this pipeline seamlessly generates distinct conversational datasets, bypasses mode-collapse, trains distinct LoRA adapter layers, runs terminal inferences locally, and flawlessly exposes the AI engine directly to a stunning aesthetic 3D Web Browser UI!

## 📂 Directory Structure

```text
├── gen_data.py               # Generates pristine 400-row distinct Rocky permutations (Science, Humor, Emotion)
├── dedupe.py                 # Validates the generation bounds keeping semantic duplication tightly at 0%
├── evaluate_rocky.py         # Automated edge-case benchmarking tool for the 7B LoRA safety boundaries
├── finetune_rocky.py         # LoRA MLX tuning pipeline for the heavy 7B foundational model
├── finetune_rocky_mini.py    # Accelerated LoRA tuning loop specifically targeted for the 1.5B edge model
├── chat_rocky.py             # ChatML CLI terminal interface connecting to the 7B context memory
├── chat_rocky_mini.py        # ChatML CLI terminal interface connecting to the 1.5B context memory
├── server.py                 # Consolidated FastAPI dual-bridge tracking both 1.5B and 7B VRAM instances
├── export_web.py             # Automates LoRA parameter-fusing and prints the exact TVM pipeline for WebGPU .wasm exports
├── rocky_datasets/           # Unpacked directory containing the raw JSONL split fragments
├── web/                      # The dynamic frontend 3D UI aesthetic interface
│   ├── index.html            # Hosts the live SVG text-path Petrova Star and dual-orbiting CSS starships
│   ├── style.css             # Glassmorphism UX, CSS spatial perspectives, deep atmospheric grading
│   └── script.js             # Translates 3D chat DOM nodes mathematically merging into the asymptote of the golden Petrova Sun
```

## 🚀 Getting Started

### 1. Environment & Packages
Create an isolated virtual environment to prevent package cross-contamination, then pip load the Apple MLX environment maps:
```bash
python3 -m venv rocky-mlx
source rocky-mlx/bin/activate
pip install mlx mlx-lm transformers datasets fastapi uvicorn "huggingface_hub[cli]"
```

### 2. Generate the Rocky Core
Rather than downloading a static dataset, locally construct your own totally unique 400-slice Rocky memory pool. This will build `train.jsonl` and `valid.jsonl`:
```bash
python3 gen_data.py
```

### 3. Model Conversion
Pull the base Qwen models completely unauthenticated from HuggingFace and perfectly compile them iteratively into MLX 4-bit Safetensors format:

**For the Heavy (7B) core:**
```bash
python3 -m mlx_lm convert --hf-path Qwen/Qwen2.5-7B-Instruct --mlx-path ./qwen2.5-7b-mlx -q
```
**For the Rapid Edge (1.5B) core:**
```bash
python3 -m mlx_lm convert --hf-path Qwen/Qwen2.5-1.5B-Instruct --mlx-path ./qwen2.5-1.5b-mlx -q
```

### 4. Finetuning Training Pass
Inject the 400 context elements securely into the neural net:
```bash
python3 finetune_rocky_mini.py   # Compiles the fast 1.5B Edge Node
# or
python3 finetune_rocky.py        # Compiles the 7B Base Node
```

### 5. Chat locally via your CLI!
Begin interacting directly in your MacOS terminal:
```bash
python3 chat_rocky.py
```

### 6. The Web UI (Blip-A Interface)
To leverage the stunning 3D Petrova Line interface overlay, launch your consolidated FastAPI bridging node.

To power the website with the **Heavy 7B Base Model**, run:
```bash
python3 server.py
```

To power the website with the blazing **Fast 1.5B Edge Model**, simply pass the mini flag:
```bash
python3 server.py --mini
```

**CRITICAL WEB LAUNCH STEP:**
Do not double click the local `index.html` file in your Mac Finder! Chrome security policies strictly block `file://` fetching. Instead, once the python script prints `FASTAPI ENGINE READY!`, immediately type `http://127.0.0.1:8000` directly into your web browser's URL bar! The Python Engine organically hosts the HTML graphics itself right alongside the AI API routing!

### 7. Exporting Core directly into an Edge Browser
If you want to strip away the Python overhead entirely and cross-compile your finalized MLX arrays into pure `.wasm` shaders for native WebGPU execution (e.g. for WebLLM implementation):
```bash
python3 export_web.py
```
This executes Phase One (Fusing limits) natively across MLX, and outputs the exact `mlc-llm` compiler shell pipelines necessary for Phase Two.
