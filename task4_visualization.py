import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_visualizations(summary_file, detailed_file):
    plot_dir = 'data/plots'
    os.makedirs(plot_dir, exist_ok=True)

    try:
        summary_df = pd.read_csv(summary_file)
        detailed_df = pd.read_csv(detailed_file)
    except FileNotFoundError as e:
        print(f"Error loading data: {e}. Ensure task 3 has run successfully.")
        return

    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(10, 6))
    sns.barplot(data=summary_df, x='category', y='total_engagement', hue='category', palette='viridis', legend=False)
    
    plt.title('Total Engagement (Score + Comments) by Category', fontsize=14, pad=15)
    plt.xlabel('Category', fontsize=12)
    plt.ylabel('Total Engagement', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    bar_chart_path = os.path.join(plot_dir, 'engagement_by_category.png')
    plt.savefig(bar_chart_path)
    plt.close()
    print(f"Saved Bar Chart: {bar_chart_path}")

    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=detailed_df, 
        x='score', 
        y='num_comments', 
        hue='category', 
        s=100, 
        alpha=0.7, 
        palette='tab10'
    )
    
    plt.title('Hacker News Posts: Score vs. Number of Comments', fontsize=14, pad=15)
    plt.xlabel('Post Score', fontsize=12)
    plt.ylabel('Number of Comments', fontsize=12)
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    scatter_chart_path = os.path.join(plot_dir, 'score_vs_comments.png')
    plt.savefig(scatter_chart_path)
    plt.close()
    print(f"Saved Scatter Plot: {scatter_chart_path}")

if __name__ == "__main__":
    summary_csv = 'data/category_summary.csv'
    detailed_csv = 'data/analyzed_trends.csv'
    
    create_visualizations(summary_csv, detailed_csv)