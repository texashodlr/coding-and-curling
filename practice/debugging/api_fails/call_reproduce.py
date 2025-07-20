import logging
import requests
import os

logging.basicConfig(level=logging.INFO, filename='api.log')

url = "https://api.openai.com/v1/chat/completions"

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPEN_AI_KEY env var not set.")

headers = {
        "Content-Type": "application/json", 
        "Authorization": f"Bearer {api_key}"
        }

payload = {
        "model": "gpt-4o", 
        "messages": [{"role": "user", "content": "Howdy!"}], 
        "max_tokens": 50}

try:
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status() # Raising exception for 4XX/5XX Errors
    logging.info(f"Success: Status {response.status_code}, Response: {response.json()}")
except requests.exceptions.RequestException as e:
    logging.error(f"API Call failed: {str(e)}")
    raise
