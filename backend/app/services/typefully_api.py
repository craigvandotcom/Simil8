import json
import urllib3
import logging
import asyncio
from typing import List, Dict, Any
from ..config import Config
from ..logger import get_logger
from .error_reporting import report_error_to_discord

http = urllib3.PoolManager()

logger = get_logger(__name__)

async def create_typefully_draft(tweets: List[str], account: str = 'account1', schedule: bool = False, schedule_date: str = "next-free-slot", auto_retweet: bool = False) -> Dict[str, Any]:
    try:
        url = "https://api.typefully.com/v1/drafts"
        
        # Choose the appropriate API key based on the account parameter
        if account == 'account2':
            api_key = Config.TYPEFULLY_API_KEY_ACCOUNT2
        else:
            api_key = Config.TYPEFULLY_API_KEY

        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }
        content = "\n\n\n\n".join(tweets)
        data = {
            "content": content,
            "threadify": False,
            "share": True,
            "auto_retweet_enabled": False,
            "auto_plug_enabled": True
        }

        # Add scheduling information if requested
        if schedule:
            data["schedule-date"] = schedule_date

        # Add logging
        logger.info(f"Sending draft to Typefully for account: {account}", extra={
            "content_length": len(content),
            "scheduling": schedule,
            "schedule_date": schedule_date if schedule else "N/A",
            "auto_retweet": auto_retweet
        })

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
        error_message = f"Error creating Typefully draft for account {account}: {str(e)}"
        logger.error(error_message, exc_info=True)
        # Call the async function properly
        await report_error_to_discord(error_message)
        raise