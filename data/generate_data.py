import pandas as pd
import numpy as np
import os

def create_dataset(filename="data/dataset.csv", num_rows=1_000_000):
    print(f"Generating {num_rows} rows...")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    df = pd.DataFrame({
        "id": np.arange(num_rows),
        "category": np.random.choice(["A", "B", "C", "D", "E"], size=num_rows),
        "value": np.random.normal(loc=100, scale=15, size=num_rows),
        "multiplier": np.random.uniform(1.0, 5.0, size=num_rows)
    })
    
    df.to_csv(filename, index=False)
    print(f"Dataset saved to {filename} ({os.path.getsize(filename) / (1024*1024):.2f} MB)")

if __name__ == "__main__":
    create_dataset()