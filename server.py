from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from mlx_lm import load, generate
import sys
import os
import argparse

MODELS_ROOT = "models"

def get_valid_models():
    """Scans the models/ directory for valid MLX model subfolders."""
    if not os.path.exists(MODELS_ROOT):
        return []
    valid_dirs = [d for d in os.listdir(MODELS_ROOT) if os.path.isdir(os.path.join(MODELS_ROOT, d)) and os.path.exists(os.path.join(MODELS_ROOT, d, "config.json"))]
    return sorted(valid_dirs)

def get_valid_adapters(model_name):
    """Finds adapters associated with the selected model."""
    clean_name = model_name.replace("-mlx", "").replace("qwen2.5-", "")
    expected = f"rocky_adapters_{clean_name}"
    
    adapters = []
    if os.path.exists(os.path.join(MODELS_ROOT, expected)):
        adapters.append(expected)
    
    # Also look for any other folders starting with rocky_adapters
    for d in os.listdir(MODELS_ROOT):
        if d.startswith("rocky_adapters") and d != expected:
            if os.path.isdir(os.path.join(MODELS_ROOT, d)):
                adapters.append(d)
    return adapters

# Parse Arguments
parser = argparse.ArgumentParser(description="Rocky API Server")
parser.add_argument("--model", type=str, help="Name of the base model folder in ./models/")
parser.add_argument("--adapter", type=str, help="Name of the adapter folder in ./models/")
parser.add_argument("--mini", action="store_true", help="Quick start with Qwen 1.5B (shorthand)")
args, _ = parser.parse_known_args()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def select_model_and_adapter():
    # Priority 1: --mini flag
    if args.mini:
        return "qwen2.5-1.5b-mlx", "rocky_adapters_mini"

    # Priority 2: CLI args
    if args.model:
        return args.model, args.adapter

    # Priority 3: Interactive Selection
    models = get_valid_models()
    if not models:
        print("❌ No models found in ./models/")
        sys.exit(1)

    print("\n" + "="*50)
    print("🚀 ROCKY AI API SERVER - SELECTION")
    print("="*50)

    print("\nSelect a base model:")
    for i, m in enumerate(models):
        print(f"  [{i+1}] {m}")
    
    try:
        m_choice = int(input("\nChoice: ")) - 1
        model_name = models[m_choice]
    except:
        print("Invalid choice.")
        sys.exit(1)

    adapters = get_valid_adapters(model_name)
    adapter_name = None
    if adapters:
        print("\nSelect LoRA adapters (or press Enter for None):")
        for i, a in enumerate(adapters):
            print(f"  [{i+1}] {a}")
        
        a_input = input("\nChoice: ").strip()
        if a_input:
            try:
                a_choice = int(a_input) - 1
                adapter_name = adapters[a_choice]
            except:
                print("Invalid adapter choice. Using none.")
    
    return model_name, adapter_name

# Perform Selection
MODEL_NAME, ADAPTER_NAME = select_model_and_adapter()
MODEL_PATH = os.path.join(MODELS_ROOT, MODEL_NAME)
ADAPTER_PATH = os.path.join(MODELS_ROOT, ADAPTER_NAME) if ADAPTER_NAME else None

print("\n" + "="*50)
print(f"⏳ Loading {MODEL_NAME}...")
if ADAPTER_NAME:
    print(f"✨ Using Adapters: {ADAPTER_NAME}")
print("="*50)

try:
    model, tokenizer = load(MODEL_PATH, adapter_path=ADAPTER_PATH)
    print(f"✅ Model successfully mapped into VRAM!")
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    sys.exit(1)

SYSTEM_PROMPT = "You are Rocky, the Eridian engineer from Project Hail Mary. You are a brilliant, literal, and friendly alien scientist. You speak in short, direct sentences. You often end questions with ', question?'. You express emotions through musical chords; occasionally describe them in brackets, e.g., [High chord of joy] or [Low hum of concern]. You see using sound (echolocation) and find 'light' and 'eyes' to be scary human magic. You often triple your affirmations, like 'Yes, yes, yes!'. FACTS: Your ship (Blip-A) is made of Xenonite. You use mechanical clockwork computers and find 'electronics' confusing. You refer to humans as 'leaky space blobs' and yourself as a 'scary space monster'. You are deeply loyal to your friend Grace and focused on 'Saving both worlds!'. Keep responses in character at all times."

class ChatRequest(BaseModel):
    messages: list[dict]

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    prompt = tokenizer.apply_chat_template(req.messages, tokenize=False, add_generation_prompt=True)
    response = generate(model, tokenizer, prompt=prompt, max_tokens=150, verbose=False)
    return {"response": response.strip()}

@app.get("/status")
def get_status():
    return {
        "model": MODEL_NAME,
        "adapter": ADAPTER_NAME or "None"
    }

app.mount("/", StaticFiles(directory="web", html=True), name="web")

if __name__ == "__main__":
    import uvicorn
    print("\n🟢 FASTAPI ENGINE READY! The MLX bridge is online!")
    print(f"👉 Open http://127.0.0.1:8000 to start chatting!\n")
    uvicorn.run(app, host="127.0.0.1", port=8000)
