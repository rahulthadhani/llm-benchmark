def build_prompt(prompt: str, category: str, examples: dict) -> str:
    shots = examples.get(category, [])
    
    prefix = "\n\n".join([
        f"Q: {e['prompt']}\nA: {e['answer']}" 
        for e in shots
    ])
    
    return f"{prefix}\n\nQ: {prompt}\nA:"