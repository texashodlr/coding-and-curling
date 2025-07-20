import unittest
from unittest.mock import patch
import os
import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import logging
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

class TestAPICall(unittest.TestCase):
    @patch('requests.post')
    def test_rate_limit(self, mock_post):
        mock_post.return_value.status_code=429
        mock_post.return_value.headers    ={"Retry-After": "5"}
        with self.assertRaises(Exception):
            make_api_call(url, payload,headers)
