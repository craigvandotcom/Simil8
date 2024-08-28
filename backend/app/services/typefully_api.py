import json
import urllib3
import logging
import asyncio
from typing import List, Dict, Any
from ..config import Config
from ..logger import get_logger
from ..services.discord_bot import report_error_to_discord

http = urllib3.PoolManager()

logger = get_logger(__name__)

async def create_typefully_draft(tweets: List[str]) -> Dict[str, Any]:
    try:
        url = "https://api.typefully.com/v1/drafts"
        headers = {
            "X-API-KEY": Config.TYPEFULLY_API_KEY,
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
        logger.info("Sending draft to Typefully", extra={"content_length": len(content)})
        response = http.request(
            'POST',
            url,
            body=json.dumps(data).encode('utf-8'),
            headers=headers
        )
        if response.status != 200:
            raise urllib3.exceptions.HTTPError(f"HTTP error {response.status}: {response.data.decode('utf-8')}")
        return json.loads(response.data.decode('utf-8'))
    except Exception as e:
        error_message = f"Error creating Typefully draft: {str(e)}"
        logger.error(error_message, exc_info=True)
        await report_error_to_discord(error_message)
        raise