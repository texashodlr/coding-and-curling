import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, filename='ingestion.log')

def extract_data(file_path):
    df = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='warn')
    logging.info(f"Extracted {len(df)} rows, columns: {df.columns.tolist()}")
    return df

def transform_data(df):
    df['sold_date'] = pd.to_datetime(df['sold_date'], errors='coerce')
    logging.info(f"Transformed data, missing dates: {df['sold_date'].isna().sum()}")
    return df

def load_data(df, output_path):
    df.to_parquet(output_path)
    logging.info(f"Loaded data to {output_path}")

# Running the pipeline
df = extract_data('data.csv')
df = transform_data(df)
load_data(df, 'processed_data.parquet')
