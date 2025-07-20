import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, filename='ingestion.log')
expected_cols = ['apple', 'banana', 'grapes', 'pineapple', 'peach']
df = pd.read_csv('data.csv')
if set(df.columns) != set(expected_cols):
    missing = set(expected_cols) - set(df.columns)
    extra = set(df.columns) - set(expected_cols)
    logging.error(f"Schema mismatch - Missing: {missing}, Extra: {extra}")
    raise ValueError("Schema mismatch")

print(df.dtypes)
