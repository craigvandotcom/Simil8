import logging
from ..config import Config
from datetime import datetime, timedelta
from typing import Any, Dict, List
import requests
import asyncio
from .tweet_generator import to_tweet_variations
from .typefully_api import create_typefully_draft
from ..logger import get_logger
from .error_reporting import report_error_to_discord  # Update this import

logger = get_logger(__name__)

def fetch_from_export_api(updated_after: str | None = None) -> List[Dict[str, Any]]:
    """
    Fetches data from the Readwise Export API.
    
    Args:
        updated_after (str | None): ISO format datetime string to filter results.
    
    Returns:
        List[Dict[str, Any]]: List of book data dictionaries.
    """
    full_data = []
    next_page_cursor = None
    while True:
        params = {}
        if next_page_cursor:
            params['pageCursor'] = next_page_cursor
        if updated_after:
            params['updatedAfter'] = updated_after
        logger.info("Making export API request", extra={"params": params})
        response = requests.get(
            url="https://readwise.io/api/v2/export/",
            params=params,
            headers={"Authorization": f"Token {Config.READWISE_TOKEN}"},
            verify=False  # Note: In production, you might want to verify SSL certificates
        )
        response.raise_for_status()
        data = response.json()
        full_data.extend(data['results'])
        next_page_cursor = data.get('nextPageCursor')
        if not next_page_cursor:
            break
    return full_data

def process_highlights() -> List[Dict[str, Any]]:
    # Calculate the timestamp for 'READWISE_TASK_FREQUENCY' minutes ago
    time_interval_ago = (datetime.utcnow() - timedelta(minutes=Config.READWISE_TASK_FREQUENCY)).strftime('%Y-%m-%dT%H:%M:%SZ')
    logger.info("Fetching highlights updated after", extra={"time": time_interval_ago})
    
    try:
        data = fetch_from_export_api(updated_after=time_interval_ago)
        processed_highlights = []
        
        for book in data:
            for highlight in book['highlights']:
                processed_highlight = {
                    'id': highlight['id'],
                    'text': highlight['text'],
                    'book_title': book['title'],
                    'book_author': book['author'],
                    'source': book['source'],
                    'category': book['category']
                }
                processed_highlights.append(processed_highlight)
        
        logger.info("Processed highlights", extra={"count": len(processed_highlights)})
        return processed_highlights
    except Exception as e:
        error_message = f"Error processing highlights: {str(e)}"
        logger.error(error_message, exc_info=True)
        asyncio.create_task(report_error_to_discord(error_message))
        return []

async def run_frequent_task():
    while True:
        try:
            logger.info("Starting frequent task")
            if Config.ENABLE_READWISE_INTEGRATION:
                highlights = process_highlights()
                results = []

                for highlight in highlights:
                    variations = to_tweet_variations(highlight['text'], highlight=highlight)
                    logger.info("Generated variations for highlight", extra={"highlight_id": highlight['id'], "variations": variations})

                    if Config.ENABLE_TYPEFULLY_INTEGRATION:
                        response = create_typefully_draft(variations)
                        result = {
                            "status": "success",
                            "highlight_id": highlight['id'],
                            "draft_id": response.get("id"),
                            "share_url": response.get("share_url"),
                            "tweet_count": len(variations)
                        }
                        results.append(result)

                logger.info("Task completed", extra={"results": results})
        except Exception as e:
            error_message = f"Error in frequent task: {str(e)}"
            logger.error(error_message, exc_info=True, extra={"error_message": str(e)})
            await report_error_to_discord(error_message)

        # Wait for the specified interval before running again
        await asyncio.sleep(Config.READWISE_TASK_FREQUENCY * 60)  # Convert minutes to seconds
