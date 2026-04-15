import json
import random
import os
import subprocess
from pathlib import Path

DATA_FILE = "rocky_datasets/rocky_full_dataset_clean.jsonl"
OUT_DIR = "rocky_data_split"
MODEL_PATH = "./models/qwen2.5-7b-mlx"
ADAPTER_PATH = "./models/rocky_adapters"

def main():
    if not os.path.exists(DATA_FILE):
        print(f"Error: Could not find {DATA_FILE}")
        print("Please ensure gen_data.py has generated the datasets first.")
        return

    # 1. Prepare data splits
    from typing import List
    print(f"Reading dataset from {DATA_FILE}...")
    lines: List[str] = []
    with open(DATA_FILE, "r") as f:
        for line in f:
            lines.append(line)
        
    random.shuffle(lines)
    
    # Take defaults of 90% train, 10% valid for a 1000 sample dataset
    train_split = [lines[i] for i in range(len(lines)-100)]
    valid_split = [lines[i] for i in range(len(lines)-100, len(lines))]
    
    Path(OUT_DIR).mkdir(exist_ok=True)
    
    with open(os.path.join(OUT_DIR, "train.jsonl"), "w") as f:
        f.writelines(train_split)
        
    with open(os.path.join(OUT_DIR, "valid.jsonl"), "w") as f:
        f.writelines(valid_split)
        
    print(f"Data split successful: {len(train_split)} train, {len(valid_split)} valid")
    print(f"Saved into folder: {OUT_DIR}/")
    
    # 2. Run finetuning via MLX
    if not os.path.exists(MODEL_PATH):
        print(f"\nWarning: The base model path '{MODEL_PATH}' was not found.")
        print("Before running fine-tuning, make sure you convert the HuggingFace model into MLX format!")
        print("Run this command exactly as written in your virtual environment:")
        print("python3 -m mlx_lm convert --hf-path Qwen/Qwen2.5-7B-Instruct --mlx-path ./models/qwen2.5-7b-mlx -q")
        return
        
    print("\nStarting MLX LoRA Fine-tuning Phase...")
    cmd = [
        "python3", "-m", "mlx_lm", "lora",
        "--model", MODEL_PATH,
        "--train",
        "--data", OUT_DIR,
        "--batch-size", "4",
        "--num-layers", "16",
        "--iters", "1000",             # Adjust iteration count depending on preference (1000 is robust for 900 samples)
        "--learning-rate", "1e-5",
        "--adapter-path", ADAPTER_PATH
    ]
    
    print(f"\nExecuting command:")
    print(" ".join(cmd))
    print("\nStarting now (this might take several minutes depending on your mac)...")
    
    try:
        subprocess.run(cmd, check=True)
        print(f"\n✅ Fine-tuning completed! LoRA Adapters saved to {ADAPTER_PATH}")
        print("\nTo chat with the newly trained Rocky model, run:")
        print(f"python3 -m mlx_lm.generate --model {MODEL_PATH} --adapter-path {ADAPTER_PATH} --prompt 'Hey Rocky!'")
    except subprocess.CalledProcessError as e:
        print(f"\nFailed to run fine-tuning string! Error code: {e.returncode}")

if __name__ == "__main__":
    main()
