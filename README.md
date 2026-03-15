\# LLM Prompt Engineering Benchmark



A benchmark suite that evaluates how different prompting strategies affect 

LLM accuracy across reasoning, coding, factual, and ambiguous question categories.



\## What it does



Tests 200 prompts across 4 categories using 4 prompting strategies:

\- \*\*Zero-shot\*\* — raw prompt, no examples or instructions

\- \*\*Few-shot\*\* — 2–3 demonstrations prepended before the question

\- \*\*Chain-of-thought\*\* — appends "Let's think step by step" to the prompt

\- \*\*Role prompting\*\* — assigns a domain expert persona before the question



Evaluates outputs using exact match, code structure checks, and an LLM judge 

for open-ended responses. Results are visualized as bar charts and a heatmap.



\## Key findings



\- Chain-of-thought improved reasoning accuracy over zero-shot baseline

\- Few-shot showed example bias on reasoning tasks, scoring lower than expected

\- Role prompting added minimal benefit on logic-heavy questions

\- Coding tasks were robust across all four strategies



\## Tech stack



\- Python 3.11

\- OpenAI API (gpt-4o-mini)

\- Pandas — data loading and result aggregation

\- Matplotlib + Seaborn — visualization

\- python-dotenv — API key management



\## Project structure

```

llm-benchmark/

├── data/

│   ├── prompts.csv              # 200 prompts across 4 categories

│   └── few\_shot\_examples.json   # demonstration examples per category

├── strategies/

│   ├── zero\_shot.py

│   ├── few\_shot.py

│   ├── chain\_of\_thought.py

│   └── role\_prompting.py

├── evaluation/

│   ├── evaluator.py             # exact match + code check scoring

│   └── llm\_judge.py             # GPT-based scoring for open questions

├── results/

│   ├── raw\_outputs.csv          # raw LLM responses

│   ├── scored\_results.csv       # responses with scores attached

│   ├── chart\_overall.png

│   ├── chart\_by\_category.png

│   └── chart\_heatmap.png

├── runner.py                    # orchestrates all API calls

└── analysis.py                  # generates charts and summary tables

```



\## How to run



1\. Clone the repo and install dependencies:

```bash

pip install -r requirements.txt

```



2\. Add your OpenAI API key to a `.env` file:

```

OPENAI\_API\_KEY=your-key-here

```



3\. Run the benchmark:

```bash

python runner.py

```



4\. Score the results:

```bash

python -m evaluation.score\_results

```



5\. Generate charts:

```bash

python analysis.py

```



\## Resume line



Built a benchmark suite evaluating prompt strategies across 200 reasoning, 

coding, factual, and ambiguous tasks — measuring accuracy differences between 

zero-shot, few-shot, chain-of-thought, and role prompting using the OpenAI API, 

Pandas, and Matplotlib.

