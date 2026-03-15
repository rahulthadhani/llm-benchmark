ROLES = {
    "reasoning": "You are a logical reasoning expert who thinks carefully before answering.",
    "coding":    "You are a senior software engineer who writes clean, correct Python code.",
    "factual":   "You are a knowledgeable encyclopedia that gives precise, accurate answers.",
    "ambiguous": "You are a thoughtful philosopher who explores questions from multiple angles.",
}

def build_prompt(prompt: str, category: str) -> str:
    role = ROLES.get(category, "You are a helpful assistant.")
    return f"System: {role}\n\nUser: {prompt}"