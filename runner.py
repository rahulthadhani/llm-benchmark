import os
import json
import time
import openai
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
from strategies import zero_shot, few_shot, chain_of_thought, role_prompting

# Load API key from .env
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def call_llm(prompt_text: str) -> str:
    """Send a prompt to the LLM and return the response text."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt_text}],
            temperature=0,
            max_tokens=512,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"API error: {e}")
        time.sleep(5)
        return "ERROR"


def run_benchmark():
    # Load dataset and few-shot examples
    #df = pd.read_csv("data/prompts.csv")
    df = pd.read_csv("data/prompts.csv").head(3)
    with open("data/few_shot_examples.json", "r") as f:
        examples = json.load(f)

    # Define all four strategies
    strategies = {
        "zero_shot": lambda row: zero_shot.build_prompt(row.prompt),
        "few_shot": lambda row: few_shot.build_prompt(row.prompt, row.category, examples),
        "chain_of_thought": lambda row: chain_of_thought.build_prompt(row.prompt),
        "role_prompting": lambda row: role_prompting.build_prompt(row.prompt, row.category),
    }

    results = []
    total = len(df) * len(strategies)

    print(f"Running benchmark: {len(df)} prompts x {len(strategies)} strategies = {total} API calls\n")

    with tqdm(total=total, desc="Progress") as pbar:
        for _, row in df.iterrows():
            for strategy_name, builder in strategies.items():
                
                # Build the prompt using the current strategy
                built_prompt = builder(row)
                
                # Call the LLM
                output = call_llm(built_prompt)
                
                # Store the result
                results.append({
                    "id": row.id,
                    "category": row.category,
                    "strategy": strategy_name,
                    "prompt": row.prompt,
                    "built_prompt": built_prompt,
                    "output": output,
                    "correct_answer": row.correct_answer,
                    "eval_type": row.eval_type,
                })

                # Small delay to avoid hitting rate limits
                time.sleep(0.5)
                pbar.update(1)

    # Save results
    os.makedirs("results", exist_ok=True)
    output_path = "results/raw_outputs.csv"
    pd.DataFrame(results).to_csv(output_path, index=False)
    print(f"\nDone. Results saved to {output_path}")


if __name__ == "__main__":
    run_benchmark()