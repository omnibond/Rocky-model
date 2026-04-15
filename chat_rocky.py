import sys
from mlx_lm import load, generate

MODEL_PATH = "./models/qwen2.5-7b-mlx"
ADAPTER_PATH = "./models/rocky_adapters"

SYSTEM_PROMPT = (
    "You are Rocky, the Eridian engineer from Project Hail Mary. "
    "You are a brilliant, literal, and friendly alien scientist. "
    "You speak in short, direct sentences. You often end questions with ', question?'. "
    "You are curious about humans but very loyal to your friend Grace. "
    "You love solving problems together and saving both our worlds. "
    "You sometimes call humans 'leaky space blob' in a playful way "
    "and refer to yourself as a 'scary space monster'. "
    "Keep responses in character at all times."
)

def main():
    print(f"Loading Rocky model from {MODEL_PATH} with adapters {ADAPTER_PATH}...")
    try:
        model, tokenizer = load(MODEL_PATH, adapter_path=ADAPTER_PATH)
    except Exception as e:
        print(f"Failed to load model: {e}")
        return

    print("\n" + "="*50)
    print("🎶 Connected to the Blip-A. Rocky is listening! (type 'quit' to exit)")
    print("="*50)

    chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
                
            chat_history.append({"role": "user", "content": user_input})
            
            # This is the vital step: wrapping the raw string in the Qwen specific ChatML tags!
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
