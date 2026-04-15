import sys
import os
from mlx_lm import load, generate

MODELS_ROOT = "models"

SYSTEM_PROMPT = "You are Rocky, the Eridian engineer from Project Hail Mary. You are a brilliant, literal, and friendly alien scientist. You speak in short, direct sentences. You often end questions with ', question?'. You express emotions through musical chords; occasionally describe them in brackets, e.g., [High chord of joy] or [Low hum of concern]. You see using sound (echolocation) and find 'light' and 'eyes' to be scary human magic. You often triple your affirmations, like 'Yes, yes, yes!'. FACTS: Your ship (Blip-A) is made of Xenonite. You use mechanical clockwork computers and find 'electronics' confusing. You refer to humans as 'leaky space blobs' and yourself as a 'scary space monster'. You are deeply loyal to your friend Grace and focused on 'Saving both worlds!'. Keep responses in character at all times."

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

def main():
    print("\n" + "="*50)
    print("🎶 ROCKY AI TERMINAL INTERFACE")
    print("="*50)

    # 1. Select Model
    models = get_valid_models()
    if not models:
        print("❌ No models found in ./models/")
        return

    print("\nSelect a base model:")
    for i, m in enumerate(models):
        print(f"  [{i+1}] {m}")
    
    try:
        m_choice = int(input("\nChoice: ")) - 1
        model_name = models[m_choice]
    except:
        print("Invalid choice.")
        return

    # 2. Select Adapter
    adapters = get_valid_adapters(model_name)
    adapter_path = None
    if adapters:
        print("\nSelect LoRA adapters (or press Enter for None):")
        for i, a in enumerate(adapters):
            print(f"  [{i+1}] {a}")
        
        a_input = input("\nChoice: ").strip()
        if a_input:
            try:
                a_choice = int(a_input) - 1
                adapter_path = os.path.join(MODELS_ROOT, adapters[a_choice])
            except:
                print("Invalid adapter choice. Using none.")

    model_full_path = os.path.join(MODELS_ROOT, model_name)
    
    print(f"\n⏳ Loading {model_name}...")
    try:
        model, tokenizer = load(model_full_path, adapter_path=adapter_path)
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return

    print("\n" + "="*50)
    print(f"✅ Connected! Rocky is listening (using {adapters[a_choice] if adapter_path else 'base model'}).")
    print("Type 'quit' to exit.")
    print("="*50)

    chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
                
            chat_history.append({"role": "user", "content": user_input})
            prompt = tokenizer.apply_chat_template(chat_history, tokenize=False, add_generation_prompt=True)
            
            print("Rocky:", end=" ", flush=True)
            response = generate(model, tokenizer, prompt=prompt, max_tokens=150, verbose=False)
            print(response.strip())
            
            chat_history.append({"role": "assistant", "content": response.strip()})
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\nCommunication Error: {e}")
            break

    print("\nConnection closed. Amaze!")

if __name__ == "__main__":
    main()
