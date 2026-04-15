from mlx_lm import load, generate

MODEL_PATH = "./models/gemma-4-e4b-mlx"
ADAPTER_PATH = "./models/rocky_adapters_gemma-4-e4b"

SYSTEM_PROMPT = "You are Rocky, the Eridian engineer from Project Hail Mary. You are a brilliant, literal, and friendly alien scientist. You speak in short, direct sentences. You often end questions with ', question?'. You express emotions through musical chords; occasionally describe them in brackets, e.g., [High chord of joy] or [Low hum of concern]. You see using sound (echolocation) and find 'light' and 'eyes' to be scary human magic. You often triple your affirmations, like 'Yes, yes, yes!'. FACTS: Your ship (Blip-A) is made of Xenonite. You use mechanical clockwork computers and find 'electronics' confusing. You refer to humans as 'leaky space blobs' and yourself as a 'scary space monster'. You are deeply loyal to your friend Grace and focused on 'Saving both worlds!'. Keep responses in character at all times."

# Multi-turn scenarios
scenarios = [
    {
        "name": "Engineering Emergency",
        "turns": [
            "Rocky, the main fuel line is vibrating. Is that bad?",
            "I checked the pressure, it's spiking at 400 atmospheres. What do we do?",
            "Okay, I'm turning the valve. Is it safe now?"
        ]
    },
    {
        "name": "Human Culture Shock",
        "turns": [
            "I'm feeling a bit lonely today, Rocky. I miss seeing the sky on Earth.",
            "It was blue, with white fluffy clouds. And it felt... infinite.",
            "You're right. We have work to do. Let's look at the astrophage cultures."
        ]
    },
    {
        "name": "The 'Leaky Space Blob' Dynamic",
        "turns": [
            "Hey Rocky, am I doing this right?",
            "Wait, why did you just call me a leaky space blob?",
            "Fair enough. You're a scary space monster, after all."
        ]
    }
]

def run_scenario(model, tokenizer, scenario):
    print(f"\n--- Scenario: {scenario['name']} ---")
    chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    for turn in scenario['turns']:
        print(f"You: {turn}")
        chat_history.append({"role": "user", "content": turn})
        
        prompt = tokenizer.apply_chat_template(chat_history, tokenize=False, add_generation_prompt=True)
        response = generate(
            model, 
            tokenizer, 
            prompt=prompt, 
            max_tokens=150, 
            verbose=False
        ).strip()
        
        print(f"Rocky: {response}")
        chat_history.append({"role": "assistant", "content": response})
    print("-" * 30)

def main():
    print(f"Loading Rocky ({MODEL_PATH})...")
    try:
        model, tokenizer = load(MODEL_PATH, adapter_path=ADAPTER_PATH)
    except Exception as e:
        print(f"Error: {e}")
        return

    print("\n" + "="*50)
    print("🧪 ADVANCED ROCKY PERSONALITY TEST")
    print("="*50)

    for scenario in scenarios:
        run_scenario(model, tokenizer, scenario)

if __name__ == "__main__":
    main()
