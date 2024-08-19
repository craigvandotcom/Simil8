import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List

import requests

from config import IS_PRODUCTION, READWISE_TOKEN, frequent_task_interval

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
            headers={"Authorization": f"Token {READWISE_TOKEN}"},
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
    time_interval_ago = (datetime.utcnow() - timedelta(minutes=frequent_task_interval)).strftime('%Y-%m-%dT%H:%M:%SZ')
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