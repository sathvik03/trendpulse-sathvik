import pandas as pd
import json

def process_data(input_filepath, output_filepath):
    with open(input_filepath, 'r') as file:
        data = json.load(file)
    
    df = pd.DataFrame(data)
    
    df.dropna(subset=['post_id', 'title'], inplace=True)
    
    df.to_csv(output_filepath, index=False)
    print(f"Data successfully cleaned and saved to {output_filepath}")

if __name__ == "__main__":
    process_data('data/trends_20260405.json', 'data/cleaned_trends.csv')