import os
import openai
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def llm_judge(prompt: str, response: str) -> float:
    """Use GPT to score an open-ended response between 0 and 1."""

    judge_prompt = f"""You are an impartial evaluator. Score the quality of the response below.

Question: {prompt}
Response: {response}

Rate the response on a scale from 0 to 1 where:
- 1.0 = excellent, thoughtful, well-reasoned
- 0.5 = partial, vague, or incomplete
- 0.0 = wrong, nonsensical, or no answer

Return only a single number between 0 and 1. Nothing else."""

    try:
        result = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": judge_prompt}],
            temperature=0,
            max_tokens=10,
        )
        score = float(result.choices[0].message.content.strip())
        return max(0.0, min(1.0, score))  # clamp between 0 and 1
    except Exception as e:
        print(f"Judge error: {e}")
        return 0.5