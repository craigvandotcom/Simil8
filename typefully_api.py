import json
import urllib3
import logging
from typing import List, Dict, Any
from config import TYPEFULLY_API_KEY

http = urllib3.PoolManager()

def create_typefully_draft(tweets: List[str]) -> Dict[str, Any]:
    url = "https://api.typefully.com/v1/drafts"
    headers = {
        "X-API-KEY": TYPEFULLY_API_KEY,
        "Content-Type": "application/json"
    }
    content = "\n\n\n\n".join(tweets)
    data = {
        "content": content,
        "threadify": False,
        "share": True,
        "auto_retweet_enabled": True,
        "auto_plug_enabled": True
    }
    # Add logging
    logging.info(f"Sending to Typefully: {content}")
    response = http.request(
        'POST',
        url,
        body=json.dumps(data).encode('utf-8'),
        headers=headers
    )
    if response.status != 200:
        raise urllib3.exceptions.HTTPError(f"HTTP error {response.status}: {response.data.decode('utf-8')}")
    return json.loads(response.data.decode('utf-8'))