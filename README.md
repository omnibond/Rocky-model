# Project Hail Mary: Rocky AI 🪨🎶

This repository contains a full pipeline to fine-tune Large Language Models (LLMs) like **Qwen2.5** (7B, 1.5B, or even 0.5B) and the new **Gemma 4 E4B** specifically into **Rocky**, the beloved Eridian engineer from Andy Weir's *Project Hail Mary*. 

Operating entirely on Apple Silicon's **MLX** neural net optimization, this pipeline seamlessly generates distinct conversational datasets, trains LoRA adapter layers, runs terminal inferences locally, and flawlessly exposes the AI engine directly to a stunning aesthetic 3D Web Browser UI!

## 📂 Directory Structure

```text
├── generate_rocky_data.py    # Generates 400-row distinct Rocky permutations (Science, Humor, Emotion)
├── dedupe.py                 # Removes duplicate entries from the generated datasets
├── evaluate_rocky.py         # Basic benchmarking tool to test single-turn responses
├── test_scenarios.py         # Advanced multi-turn conversational testing with context preservation
├── finetune_rocky.py         # UNIFIED: Scans ./models/ and lets you select any model for LoRA tuning
├── chat_rocky.py             # UNIFIED: CLI interface that lets you pick a base model and active adapters
├── server.py                 # Consolidated FastAPI bridge for the 3D Web UI
├── export_web.py             # Automates LoRA parameter-fusing for WebGPU .wasm exports
├── rocky_datasets/           # Unpacked directory containing the raw JSONL split fragments
├── web/                      # The dynamic frontend 3D UI aesthetic interface
```

## 🚀 Getting Started

### 1. Environment & Packages
Create an isolated virtual environment to prevent package cross-contamination:
```bash
python3 -m venv rocky-mlx
source rocky-mlx/bin/activate
pip install mlx mlx-lm transformers datasets fastapi uvicorn "huggingface_hub[cli]"
```

### 2. Generate the Rocky Core
Locally construct your own unique 400-slice Rocky memory pool. This will build `train.jsonl` and `valid.jsonl`:
```bash
python3 generate_rocky_data.py
```

### 3. Model Conversion
Pull base models from HuggingFace and compile them into MLX 4-bit Safetensors format. The scripts will automatically detect any model folder placed in `./models/`.

**Example: Qwen 1.5B (Edge)**
```bash
python3 -m mlx_lm convert --hf-path Qwen/Qwen2.5-1.5B-Instruct --mlx-path ./models/qwen2.5-1.5b-mlx -q
```
**Example: Gemma 4 E4B (Advanced Edge)**
```bash
python3 -m mlx_lm convert --hf-path google/gemma-4-e4b-it --mlx-path ./models/gemma-4-e4b-mlx -q
```

### 4. Unified Finetuning Training Pass
Instead of separate scripts, run the unified tuner and select your target model from the list:
```bash
python3 finetune_rocky.py
```
This script automatically detects your hardware, sets appropriate hyperparameters for the model size, and saves LoRA adapters into `./models/rocky_adapters_<model_name>`.

### 5. Testing & Evaluation
Before deploying to the Web UI, you can verify Rocky's personality using the automated test scripts:

**Basic Evaluation:** Tests single-turn prompts to check general knowledge and tone.
```bash
python3 evaluate_rocky.py
```

**Advanced Scenario Testing:** Runs multi-turn conversations (Engineering, Culture, Personality) to ensure Rocky maintains context and stays in character over a long dialogue.
```bash
python3 test_scenarios.py
```

### 6. Chat locally via your CLI!
Pick your base model and your specific fine-tuned adapters at runtime:
```bash
python3 chat_rocky.py
```

### 7. The Web UI (Blip-A Interface)
Launch the FastAPI bridge to power the 3D Petrova Line interface:
```bash
python3 server.py
# Use --mini flag to target the 1.5B weights automatically
python3 server.py --mini
```

**WEB LAUNCH:** Once the script prints `FASTAPI ENGINE READY!`, open `http://127.0.0.1:8000` in your browser.

### 8. Exporting Core directly into an Edge Browser
Cross-compile your finalized MLX arrays into pure `.wasm` shaders for native WebGPU execution:
```bash
python3 export_web.py
```

## 🧠 Deep Dive: How it Works

### Personality vs. Hard Facts
Fine-tuning with a LoRA (Low-Rank Adaptation) is like applying a "personality layer" over a base model's existing knowledge. 
*   **500–1,000 samples:** Excellent for capturing Rocky's **voice** (short sentences, "question?", "leaky space blob").
*   **The "Canvas" Effect:** A base model like Gemma has billions of parameters pre-trained on generic data. If you ask a question where the base model has a very "strong" opinion (e.g., "What are spaceships made of?"), it might hallucinate "metal" or "aluminum" even if you've told it "Xenonite" a few dozen times. 
*   **The Fix:** To fully override "hard facts," you either need a much larger dataset (5,000+ rows) or a strong **System Prompt Anchor** to tell the model which parts of its "new brain" to prioritize.

### Reducing Context Window Pressure
One of the biggest advantages of this fine-tuning pipeline is **efficiency**:
*   **Without Fine-tuning:** To get a "generic" AI to act like Rocky, you would need to send a massive "Few-Shot" prompt with 50 examples of his dialogue in **every single message**. This eats up thousands of tokens, makes the model slower, and quickly hits the "Context Window" limit.
*   **With Fine-tuning:** The "Rocky-ness" is baked into the model's weights. You only need a tiny, 2-line system prompt to "trigger" the behavior. This leaves almost the entire context window free for actual conversation, allowing Rocky to remember much longer discussions!
