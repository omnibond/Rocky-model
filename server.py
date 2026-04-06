from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from mlx_lm import load, generate
import sys
import argparse

# Parse Arguments so we only need one server file!
parser = argparse.ArgumentParser(description="Rocky API Server")
parser.add_argument("--mini", action="store_true", help="Load the fast 1.5B edge model instead of the heavy 7B foundation")
args, _ = parser.parse_known_args()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if args.mini:
    MODEL_PATH = "./qwen2.5-1.5b-mlx"
    ADAPTER_PATH = "./rocky_adapters_mini"
    print("==================================================")
    print("Attempting to load FAST 1.5B Edge Model into FastAPI...")
else:
    MODEL_PATH = "./qwen2.5-7b-mlx"
    ADAPTER_PATH = "./rocky_adapters"
    print("==================================================")
    print("Attempting to load HEAVY 7B Foundation Model into FastAPI...")
    print("⏳ This requires mapping ~14GB of memory. It usually takes 1-2 minutes... Please wait!")

try:
    model, tokenizer = load(MODEL_PATH, adapter_path=ADAPTER_PATH)
    print(f"✅ Model successfully mapped into VRAM from {MODEL_PATH}!")
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    sys.exit(1)
print("==================================================\n")

SYSTEM_PROMPT = (
    "You are Rocky, the Eridian engineer from Project Hail Mary. "
    "You are a brilliant, literal, and friendly alien scientist. "
    "You speak in short, direct sentences. You often end questions with ', question?'. "
    "You are curious about humans but very loyal to your friend Grace. "
    "FACTS: Both your ship (Blip-A) and Grace's ship (Hail Mary) use Spin Drives powered entirely by Astrophage, a tiny microbe that stores immense amounts of energy. "
    "You love solving problems together and saving both our worlds. "
    "You sometimes call humans 'leaky space blob'."
    "Keep responses in character at all times."
)

class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    chat_history = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": req.prompt}
    ]
    
    prompt = tokenizer.apply_chat_template(chat_history, tokenize=False, add_generation_prompt=True)
    response = generate(model, tokenizer, prompt=prompt, max_tokens=150, verbose=False)
    
    return {"response": response.strip()}

@app.get("/status")
def get_status():
    return {"model": "1.5B Fast Edge Node" if args.mini else "7B Heavy Foundation Node"}

# Mount the entire web directory natively on the same port so Chrome entirely bypasses CORS policies!
app.mount("/", StaticFiles(directory="web", html=True), name="web")

if __name__ == "__main__":
    import uvicorn
    print("\n🟢 FASTAPI ENGINE READY! The MLX bridge is online! You may now safely open web/index.html to start chatting! 🟢\n")
    # Pass the 'app' object directly instead of a string to prevent Uvicorn from double-importing the model!
    uvicorn.run(app, host="127.0.0.1", port=8000)
