# LLM Prompt Engineering Benchmark

A Python benchmark suite that systematically measures how prompting strategy
affects LLM accuracy across 200 tasks in reasoning, coding, factual recall,
and open-ended reasoning categories.

---

## Overview

Most prompt engineering advice is anecdotal. This project makes it empirical.

It runs the same 200 questions through four distinct prompting strategies,
scores every response automatically, and visualizes the differences — showing
exactly where chain-of-thought helps, where few-shot hurts, and where strategy
makes no difference at all.

---

## Prompting strategies tested

| Strategy | Description |
|---|---|
| Zero-shot | Raw prompt with no examples or instructions — the baseline |
| Few-shot | 2–3 demonstration examples prepended before the question |
| Chain-of-thought | Appends "Let's think step by step" to trigger explicit reasoning |
| Role prompting | Assigns a domain expert persona before the question |

---

## Evaluation methods

Different question types require different definitions of "correct":

- **Exact match** — normalizes and checks if the correct answer appears in the output (factual + reasoning)
- **Code check** — verifies the output contains a function definition (coding)
- **LLM judge** — sends response to GPT for 0–1 quality scoring (ambiguous/open-ended)

---

## Key findings

- Chain-of-thought improved multi-step reasoning accuracy over the zero-shot baseline
- Few-shot showed example bias on reasoning tasks — positive examples nudged the model toward "yes" answers even when the answer was "no"
- Role prompting added minimal benefit on logic-heavy questions, performing similarly to zero-shot
- Coding tasks were robust across all four strategies — prompting style had little effect on whether the model produced valid code

---

## Results

Charts are generated automatically in the `results/` folder after running the pipeline:

- `chart_overall.png` — mean accuracy per strategy across all categories
- `chart_by_category.png` — grouped bar chart breaking down strategy vs category
- `chart_heatmap.png` — heatmap showing accuracy at every strategy/category intersection

---

## Tech stack

| Tool | Purpose |
|---|---|
| Python 3.11 | Core language |
| OpenAI API (gpt-4o-mini) | LLM inference + LLM-as-judge scoring |
| Pandas | Data loading, grouping, and aggregation |
| Matplotlib + Seaborn | Chart generation |
| python-dotenv | API key management |

---

## Project structure
```
llm-benchmark/
├── data/
│   ├── prompts.csv                 # 200 prompts across 4 categories
│   └── few_shot_examples.json      # demonstration examples per category
├── strategies/
│   ├── zero_shot.py
│   ├── few_shot.py
│   ├── chain_of_thought.py
│   └── role_prompting.py
├── evaluation/
│   ├── evaluator.py                # exact match + code check scoring
│   ├── llm_judge.py                # GPT-based scoring for open questions
│   └── score_results.py            # runs scoring across all outputs
├── results/                        # auto-generated, not committed to git
│   ├── raw_outputs.csv
│   ├── scored_results.csv
│   ├── chart_overall.png
│   ├── chart_by_category.png
│   └── chart_heatmap.png
├── runner.py                       # orchestrates all API calls
├── analysis.py                     # generates charts and summary tables
├── .env.example                    # API key template
└── requirements.txt
```

---

## How to run

**1. Clone the repo and install dependencies**
```bash
git clone https://github.com/yourusername/llm-benchmark.git
cd llm-benchmark
pip install -r requirements.txt
```

**2. Set up your API key**

Copy the example env file and add your key:
```bash
cp .env.example .env
```
Then open `.env` and replace the placeholder with your real OpenAI API key.

**3. Run the benchmark**
```bash
python runner.py
```
This makes 800 API calls (200 prompts × 4 strategies). Takes ~15 minutes
and costs approximately $0.50–$1.00 on gpt-4o-mini.

**4. Score the results**
```bash
python -m evaluation.score_results
```

**5. Generate charts**
```bash
python analysis.py
```
Charts are saved to the `results/` folder.

---

## Known limitations

- Exact match scoring can miss correct answers that are phrased differently from the expected string
- Code check only verifies a function definition exists — it does not execute or unit test the code
- LLM-as-judge scoring can favour responses that sound confident over ones that are genuinely correct
- Results may vary across runs due to model non-determinism (temperature is set to 0 to minimise this)

---

## Resume line

> Built a benchmark suite evaluating prompt engineering strategies across 200
> reasoning, coding, factual, and ambiguous tasks — measuring accuracy
> differences between zero-shot, few-shot, chain-of-thought, and role prompting
> using the OpenAI API, Pandas, and Matplotlib.
