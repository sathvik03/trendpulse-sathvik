import pandas as pd
import numpy as np
import os

def analyze_data(input_file, output_summary, output_enriched):
    print(f"Loading data from {input_file}...")
    
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: {input_file} not found. Please run task 2 first.")
        return

    df['total_engagement'] = np.add(df['score'], df['num_comments'])

    category_summary = df.groupby('category').agg({
        'score': ['sum', 'mean'],
        'num_comments': ['sum', 'mean'],
        'total_engagement': 'sum',
        'post_id': 'count'
    }).reset_index()

    category_summary.columns = [
        'category', 'total_score', 'avg_score', 
        'total_comments', 'avg_comments', 
        'total_engagement', 'post_count'
    ]

    category_summary.to_csv(output_summary, index=False)
    
    df.to_csv(output_enriched, index=False)

    print("\n--- Category Summary ---")
    print(category_summary)
    print(f"\nSaved summary to {output_summary}")
    print(f"Saved enriched data to {output_enriched}")

if __name__ == "__main__":
    input_csv = 'data/cleaned_trends.csv'
    summary_csv = 'data/category_summary.csv'
    enriched_csv = 'data/analyzed_trends.csv'
    
    analyze_data(input_csv, summary_csv, enriched_csv)