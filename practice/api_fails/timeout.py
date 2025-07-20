import os
import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import logging
logging.basicConfig(level=logging.INFO, filename='api.log')


session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[502,503,504])
session.mount("https://", HTTPAdapter(max_retries=retries))

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
    response = session.post(url, json=payload, headers=headers, timeout=10)
    response.raise_for_status()
    logging.info(f"Success: {response.json()}")
except requests.exceptions.Timeout:
    logging.error("Request timed out")
    raise
except requests.exceptions.RequestException as e:
    logging.error(f"API error: {str(e)}")
    raise
