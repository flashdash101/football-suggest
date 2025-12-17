import pandas as pd
import numpy as np
import os

def load_data(filepath):
    df = pd.read_csv(filepath)
    
    # Identify numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    # Fill NA values in numeric columns with their respective means
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].mean())
    
    return df

# Determine the correct path for the CSV file
# Get the directory where this script is located
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, 'complete_player_stats10.csv')

# Load the data when the module is imported
player_data = load_data(csv_path)