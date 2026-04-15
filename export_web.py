import os
import subprocess
import sys

MODEL_PATH = "./models/qwen2.5-1.5b-mlx"
ADAPTER_PATH = "./models/rocky_adapters_mini"
FUSED_PATH = "./models/rocky-1.5b-fused"

def main():
    print("==================================================")
    print("🚀 STEP 1: FUSING MLX LORA ADAPTERS")
    print("==================================================")
    print("We must permanently embed your fine-tuned Rocky personality directly into the base weights.")
    
    if not os.path.exists(ADAPTER_PATH):
        print(f"❌ Error: Cannot find {ADAPTER_PATH}. Have you finished running finetune_rocky_mini.py?")
        sys.exit(1)
        
    fuse_cmd = [
        sys.executable, "-m", "mlx_lm", "fuse",
        "--model", MODEL_PATH,
        "--adapter-path", ADAPTER_PATH,
        "--save-path", FUSED_PATH
    ]
    
    try:
        subprocess.run(fuse_cmd, check=True)
        print(f"\n✅ Successfully fused MLX model into: {FUSED_PATH}")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Fusing failed: {e}")
        sys.exit(1)

    print("\n==================================================")
    print("🌐 STEP 2: WEBGPU COMPILATION INSTRUCTIONS")
    print("==================================================")
    print("The model is now a single, solid entity! However, MLX is strictly for Apple Silicon.")
    print("To convert these weights into an in-browser WebGPU format, you need to use MLC-LLM's compiler.\n")
    
    print("Because MLC-LLM relies on a complex C++ TVM compiler under the hood, I cannot run it natively")
    print("for you without risking breaking your python environment. But here is the exact process:\n")
    
    print("1. Install the MLC compiler engine:")
    print("   pip install --pre --force-reinstall mlc-ai-nightly -f https://mlc.ai/wheels\n")
    
    print("2. Compile your new fused Rocky model down into a blazing fast .wasm binary:")
    print(f"   mlc_llm compile {FUSED_PATH} --device webgpu -o dist/rocky-web.wasm\n")
    
    print("3. Fragment the weights into tiny chunks for the browser to download easily:")
    print(f"   mlc_llm convert_weight {FUSED_PATH} --quantization q4f16_1 -o dist/rocky-web-weights/\n")
    
    print("Boom! You can then upload those dist/ folders to any CDN, and use WebLLM in Javascript")
    print("to pull Rocky directly into any smartphone or laptop browser natively!")

if __name__ == "__main__":
    main()
