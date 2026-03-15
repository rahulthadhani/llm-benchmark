import re


def normalize(text: str) -> str:
    """Lowercase and strip punctuation for fair comparison."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s]', '', text)
    return text


def score_row(row) -> float:
    """Score a single result row based on its eval_type."""

    eval_type = row['eval_type']
    output = str(row['output']).strip()
    correct = str(row['correct_answer']).strip()

    if eval_type == 'exact':
        return float(normalize(correct) in normalize(output))

    elif eval_type == 'code_check':
        return float('def ' in output)

    elif eval_type == 'open':
        # Open-ended questions are scored by the LLM judge
        from evaluation.llm_judge import llm_judge
        return llm_judge(row['prompt'], output)

    return 0.0