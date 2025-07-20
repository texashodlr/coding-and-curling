import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, filename='ingestion.log')

try:
    df = pd.read_csv('data.csv', on_bad_lines='warn')
    logging.info(f"Read {len(df)} rows from data.csv")
    print(df.head())
except Exception as e:
    logging.error(f"Failed to read CSV: {str(e)}")
    raise
