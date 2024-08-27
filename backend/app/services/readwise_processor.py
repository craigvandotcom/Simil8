import logging
from ..config import Config
from datetime import datetime, timedelta
from typing import Any, Dict, List
import requests
import asyncio
from .tweet_generator import to_tweet_variations
from .typefully_api import create_typefully_draft

def fetch_from_export_api(updated_after: str | None = None) -> List[Dict[str, Any]]:
    full_data = []
    next_page_cursor = None
    while True:
        params = {}
        if next_page_cursor:
            params['pageCursor'] = next_page_cursor
        if updated_after:
            params['updatedAfter'] = updated_after
        logging.info(f"Making export api request with params {params}...")
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
    # Calculate the timestamp for 'frequent_task_interval' minutes ago
    time_interval_ago = (datetime.utcnow() - timedelta(minutes=Config.FREQUENT_TASK_INTERVAL)).strftime('%Y-%m-%dT%H:%M:%SZ')
    logging.info(f"Fetching highlights updated after: {time_interval_ago}")

    books_data = fetch_from_export_api(updated_after=time_interval_ago)
    logging.info(f"Fetched {len(books_data)} books from Readwise.")

    processed_highlights = []
    for book in books_data:
        book_title = book.get('title', 'Unknown Title')
        book_author = book.get('author', 'Unknown Author')
        book_id = book.get('user_book_id')
        for highlight in book.get('highlights', []):
            processed_highlights.append({
                'id': highlight.get('id'),
                'text': highlight.get('text', ''),
                'readwise_url': highlight.get('readwise_url', ''),
                'book_id': book_id,
                'book_title': book_title,
                'book_author': book_author,
                'highlighted_at': highlight.get('highlighted_at'),
                'color': highlight.get('color'),
                'note': highlight.get('note'),
                'tags': highlight.get('tags', [])
            })

    logging.info(f"Processed {len(processed_highlights)} highlights from {len(books_data)} books")
    return processed_highlights

async def run_frequent_task():
    while True:
        logging.info(f"Running frequent task at {datetime.now()}")
        try:
            if Config.ENABLE_READWISE_INTEGRATION:
                highlights = process_highlights()
                results = []

                for highlight in highlights:
                    thread = to_tweet_variations(highlight['text'], highlight=highlight)
                    logging.info(f"Generated thread for highlight {highlight['id']}: {thread}")

                    if Config.ENABLE_TYPEFULLY_INTEGRATION:
                        response = create_typefully_draft(thread)
                        result = {
                            "status": "success",
                            "highlight_id": highlight['id'],
                            "draft_id": response.get("id"),
                            "share_url": response.get("share_url"),
                            "tweet_count": len(thread)
                        }
                        results.append(result)

                logging.info(f"Task completed. Results: {results}")
        except Exception as e:
            logging.error(f"Error in frequent task: {str(e)}", exc_info=True)

        # Wait for the specified interval before running again
        await asyncio.sleep(Config.READWISE_TASK_FREQUENCY * 60)  # Convert minutes to seconds