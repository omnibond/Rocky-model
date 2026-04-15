import os
import subprocess
import random
import sys
from pathlib import Path
from typing import List

# ==================== CONFIGURATION ====================
DATA_FILE = "rocky_datasets/rocky_full_dataset_clean.jsonl"
OUT_DIR = "rocky_data_split"
MODELS_ROOT = "models"

def get_valid_models():
    """Scans the models/ directory for valid MLX model subfolders."""
    if not os.path.exists(MODELS_ROOT):
        return []
    
    valid_dirs = []
    for d in os.listdir(MODELS_ROOT):
        full_path = os.path.join(MODELS_ROOT, d)
        if os.path.isdir(full_path):
            # Check for config.json which is a standard MLX/HuggingFace indicator
            if os.path.exists(os.path.join(full_path, "config.json")):
                # Exclude directories that look like they're just adapters or fused results if you want
                # though usually those also have a config.json. 
                # Let's include everything with a config.json for maximum flexibility.
                valid_dirs.append(d)
    return sorted(valid_dirs)

def prepare_data():
    """Handles the 90/10 split for training and validation."""
    if not os.path.exists(DATA_FILE):
        print(f"❌ Error: Could not find {DATA_FILE}")
        print("Please ensure generate_rocky_data.py has been run first.")
        sys.exit(1)

    print(f"🔄 Reading dataset from {DATA_FILE}...")
    lines: List[str] = []
    with open(DATA_FILE, "r") as f:
        for line in f:
            lines.append(line)
        
    random.shuffle(lines)
    
    # Take defaults of 90% train, 10% valid
    num_val = max(1, len(lines) // 10)
    train_split = lines[:-num_val]
    valid_split = lines[-num_val:]
    
    Path(OUT_DIR).mkdir(exist_ok=True)
    with open(os.path.join(OUT_DIR, "train.jsonl"), "w") as f:
        f.writelines(train_split)
    with open(os.path.join(OUT_DIR, "valid.jsonl"), "w") as f:
        f.writelines(valid_split)
        
    print(f"✅ Data split successful: {len(train_split)} train, {len(valid_split)} valid")
    return len(train_split)

def main():
    print("\n" + "="*50)
    print("🚀 ROCKY AI UNIFIED FINE-TUNER")
    print("="*50)

    # 1. Discover models
    models = get_valid_models()
    if not models:
        print(f"❌ No valid MLX models found in ./{MODELS_ROOT}/")
        print("Please download a model first using 'mlx_lm convert'.")
        return

    print("\nSelect a model to fine-tune:")
    for i, m in enumerate(models):
        print(f"  [{i+1}] {m}")
    
    try:
        choice = int(input("\nEnter choice [1-{}]: ".format(len(models)))) - 1
        if choice < 0 or choice >= len(models):
            print("Invalid selection.")
            return
    except ValueError:
        print("Please enter a number.")
        return

    selected_model_name = models[choice]
    model_path = os.path.join(MODELS_ROOT, selected_model_name)
    
    # 2. Derive Adapter Path
    # If it's qwen2.5-1.5b-mlx -> rocky_adapters_1.5b
    # Simplified: rocky_adapters_<model_name_fragment>
    clean_name = selected_model_name.replace("-mlx", "").replace("qwen2.5-", "")
    adapter_path = os.path.join(MODELS_ROOT, f"rocky_adapters_{clean_name}")

    # 3. Dynamic Hyperparameters
    # We can detect model size from the name to set better defaults
    is_mini = any(x in selected_model_name.lower() for x in ["1.5b", "0.5b", "mini", "edge"])
    
    iters = "1000" # Increased for more robust personality anchoring
    lr = "2e-5" if is_mini else "1e-5"
    batch_size = "4"
    rank = 32      # Increased from default 8 for complex personality
    alpha = 64     # Target alpha
    scale = alpha / rank
    
    print(f"\nTarget Model:  {selected_model_name}")
    print(f"Output Folder: {adapter_path}")
    print(f"Iterations:    {iters}")
    print(f"Learning Rate: {lr}")
    print(f"LoRA Rank:     {rank}")
    print(f"LoRA Scale:    {scale} (alpha {alpha})")
    print("-" * 30)

    # 4. Prepare data
    num_train = prepare_data()

    # 5. Run the LoRA command
    print(f"\nStarting MLX LoRA Fine-tuning for {selected_model_name}...")
    
    # Recent mlx_lm versions (0.20+) prefer a YAML config for certain parameters
    config_path = "temp_config.yaml"
    config_content = f"""# Rocky AI Fine-tuning Config
model: "{model_path}"
train: true
data: "{OUT_DIR}"
iters: {iters}
learning_rate: {lr}
batch_size: {batch_size}
num_layers: 16
adapter_path: "{adapter_path}"
lora_parameters:
  rank: {rank}
  scale: {scale}
  dropout: 0.0
"""
    with open(config_path, "w") as f:
        f.write(config_content)

    cmd = [
        sys.executable, "-m", "mlx_lm", "lora",
        "--config", config_path
    ]
    
    print(f"\nExecuting command with config:")
    print(" ".join(cmd))
    print(f"\n--- Config Content ---\n{config_content}----------------------")
    print("\n(Note: This requires a Mac with Apple Silicon. Processing now...)\n")
    
    try:
        subprocess.run(cmd, check=True)
        print(f"\n✅ SUCCESS! Rocky adapters saved to: {adapter_path}")
        print("\nTo test your new model, run:")
        print(f"python3 chat_rocky.py  # (Note: Update chat_rocky.py to point to your new path!)")
    finally:
        if os.path.exists(config_path):
            os.remove(config_path)

if __name__ == "__main__":
    main()
