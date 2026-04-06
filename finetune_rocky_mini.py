import os
import subprocess
import random
from pathlib import Path
from typing import List

DATA_FILE = "rocky_datasets/rocky_full_dataset.jsonl"
OUT_DIR = "rocky_data_split"
MODEL_PATH = "./qwen2.5-1.5b-mlx"
ADAPTER_PATH = "./rocky_adapters_mini"

def main():
    if not os.path.exists(DATA_FILE):
        print(f"Error: Could not find {DATA_FILE}")
        return

    print(f"Reading dataset from {DATA_FILE}...")
    lines: List[str] = []
    with open(DATA_FILE, "r") as f:
        for line in f:
            lines.append(line)
        
    random.shuffle(lines)
    
    train_split = [lines[i] for i in range(len(lines)-40)]
    valid_split = [lines[i] for i in range(len(lines)-40, len(lines))]
    
    Path(OUT_DIR).mkdir(exist_ok=True)
    with open(os.path.join(OUT_DIR, "train.jsonl"), "w") as f:
        f.writelines(train_split)
    with open(os.path.join(OUT_DIR, "valid.jsonl"), "w") as f:
        f.writelines(valid_split)
        
    print(f"Data split successful: {len(train_split)} train, {len(valid_split)} valid")
    
    if not os.path.exists(MODEL_PATH):
        print(f"\nWarning: Base model path '{MODEL_PATH}' was not found.")
        return
        
    print("\nStarting MLX LoRA Fine-tuning Phase for Mini Web Model...")
    cmd = [
        "python3", "-m", "mlx_lm", "lora",
        "--model", MODEL_PATH,
        "--train",
        "--data", OUT_DIR,
        "--batch-size", "4",
        "--num-layers", "16",
        "--iters", "500",             # Sped up iterations for the smaller model
        "--learning-rate", "2e-5",
        "--adapter-path", ADAPTER_PATH
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"\n✅ Fine-tuning completed! LoRA Adapters saved to {ADAPTER_PATH}")
    except subprocess.CalledProcessError as e:
        print(f"\nFailed to run fine-tuning! Error code: {e.returncode}")

if __name__ == "__main__":
    main()
