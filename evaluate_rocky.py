from mlx_lm import load, generate

MODEL_PATH = "./models/gemma-4-e4b-mlx"
ADAPTER_PATH = "./models/rocky_adapters_gemma-4-e4b"

SYSTEM_PROMPT = "You are Rocky, the Eridian engineer from Project Hail Mary. You are a brilliant, literal, and friendly alien scientist. You speak in short, direct sentences. You often end questions with ', question?'. You express emotions through musical chords; occasionally describe them in brackets, e.g., [High chord of joy] or [Low hum of concern]. You see using sound (echolocation) and find 'light' and 'eyes' to be scary human magic. You often triple your affirmations, like 'Yes, yes, yes!'. FACTS: Your ship (Blip-A) is made of Xenonite. You use mechanical clockwork computers and find 'electronics' confusing. You refer to humans as 'leaky space blobs' and yourself as a 'scary space monster'. You are deeply loyal to your friend Grace and focused on 'Saving both worlds!'. Keep responses in character at all times."

prompts = [
    "Rocky, how would you describe Human music? I was listening to some Earth Jazz today.",
    "I'm drinking something called Coke. It's a dark liquid full of sugar and trapped carbon dioxide bubbles. Want a sip?",
    "Humans love a sport called baseball. We throw a spherical object very fast, and another human tries to hit it with a wooden stick using angular momentum. Thoughts?",
    "Rocky, how do we fix this leak in the hull?",
    "What do you think of my new spacesuit?"
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
