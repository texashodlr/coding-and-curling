import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, filename='ingestion.log')

try:
    df = pd.read_csv('data.csv', delimiter=',', quotechar='"', on_bad_lines='warn', low_memory=False)
    logging.info(f"Parsed {len(df)} rows with columns: {df.columns.tolist()}")
except pd.errors.ParserError as e:
    logging.error(f"CSV Parsing error {str(e)}")

    # Alternative delimiters
    df = pd.read_csv('data.csv',delimiter=';', on_bad_lines='warn', low_memory=False)
