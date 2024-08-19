import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

import requests

from config import IS_PRODUCTION, READWISE_TOKEN
from timestamp_storage import get_last_fetched_timestamp, update_last_fetched_timestamp

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
    last_timestamp = get_last_fetched_timestamp()

    if not last_timestamp:
        logging.info("No last fetched timestamp found. This might be the first run.")
        time_72_hours_ago = (datetime.utcnow() - timedelta(hours=72)).strftime('%Y-%m-%dT%H:%M:%SZ')
        books_data = fetch_from_export_api(updated_after=time_72_hours_ago)
    else:
        # Adjust the last timestamp to ensure strict "greater than"
        last_timestamp_dt = datetime.fromisoformat(last_timestamp.replace("Z", "+00:00"))
        adjusted_timestamp_dt = last_timestamp_dt + timedelta(seconds=1)
        adjusted_timestamp = adjusted_timestamp_dt.strftime('%Y-%m-%dT%H:%M:%SZ')

        if IS_PRODUCTION:
            books_data = fetch_from_export_api(updated_after=adjusted_timestamp)
        else:
            books_data = fetch_from_export_api()
            if books_data and books_data[0].get('highlights'):
                books_data = [{
                    **books_data[0],
                    'highlights': [books_data[0]['highlights'][0]]
                }]

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

    # Filter out highlights with 'highlighted_at' as None
    valid_highlight_times = [highlight['highlighted_at'] for highlight in processed_highlights if highlight['highlighted_at'] is not None]

    if valid_highlight_times:
        latest_highlight_time = max(valid_highlight_times)
        update_last_fetched_timestamp(latest_highlight_time)
    else:
        logging.info("No valid highlights found to update the timestamp")

    logging.info(f"Processed {len(processed_highlights)} highlights from {len(books_data)} books")
    return processed_highlights