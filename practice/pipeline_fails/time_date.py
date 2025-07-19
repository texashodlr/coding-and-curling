import pandas as pd
import logging
logging.basicConfig(level=logging.INFO, filename='ingestion.log')

df = pd.read_csv('data.csv', parse_dates=['sold_date'])
df['sold_date'] = pd.to_datetime(df['sold_date'],errors='coerce', format='%m/%d/%Y')
logging.info(f"Missing dates after parsing: {df['sold_date'].isna().sum()}")
print(df['sold_date'].head())
