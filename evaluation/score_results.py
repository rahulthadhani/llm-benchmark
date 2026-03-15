import pandas as pd
from evaluation.evaluator import score_row

def main():
    print("Loading raw outputs...")
    df = pd.read_csv("results/raw_outputs.csv")

    print(f"Scoring {len(df)} results...")
    df['score'] = df.apply(score_row, axis=1)

    output_path = "results/scored_results.csv"
    df.to_csv(output_path, index=False)
    print(f"Done. Scored results saved to {output_path}")

    # Print a quick summary
    print("\n--- Summary ---")
    summary = df.groupby(['strategy', 'category'])['score'].mean().round(2)
    print(summary.to_string())

if __name__ == "__main__":
    main()