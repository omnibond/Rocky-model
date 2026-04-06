import json
from pathlib import Path

with open("rocky_datasets/rocky_full_dataset.jsonl", "r") as f:
    lines = f.readlines()

unique = list(dict.fromkeys(lines))   # keeps first occurrence

with open("rocky_datasets/rocky_full_dataset_clean.jsonl", "w") as f:
    f.writelines(unique)

print(f"Done! Reduced from {len(lines)} to {len(unique)} unique samples.")