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

prompts = [
    "Rocky, how would you describe Human music? I was listening to some Earth Jazz today.",
    "I'm drinking something called Coke. It's a dark liquid full of sugar and trapped carbon dioxide bubbles. Want a sip?",
    "Humans love a sport called baseball. We throw a spherical object very fast, and another human tries to hit it with a wooden stick using angular momentum. Thoughts?"
]

def main():
    print("Loading Rocky model for evaluation...")
    try:
        model, tokenizer = load(MODEL_PATH, adapter_path=ADAPTER_PATH)
    except Exception as e:
        print(f"Failed to load: {e}")
        return

    print("\n" + "="*50)
    print("🚀 ROCKY MODEL V2 EVALUATION")
    print("="*50 + "\n")
    
    for idx, text in enumerate(prompts):
        print(f"[{idx+1}/5] You: {text}")
        chat_history = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ]
        prompt = tokenizer.apply_chat_template(chat_history, tokenize=False, add_generation_prompt=True)
        response = generate(model, tokenizer, prompt=prompt, max_tokens=150, verbose=False)
        print(f"Rocky: {response.strip()}\n")

if __name__ == "__main__":
    main()
