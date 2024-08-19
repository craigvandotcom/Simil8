import os

TIMESTAMP_FILE_PATH = 'last_fetched_timestamp.txt'

def get_last_fetched_timestamp() -> str:
    """Retrieve the last fetched timestamp from a file."""
    if os.path.exists(TIMESTAMP_FILE_PATH):
        with open(TIMESTAMP_FILE_PATH, 'r') as file:
            return file.read().strip()
    return ''

def update_last_fetched_timestamp(timestamp: str):
    """Update the last fetched timestamp in a file."""
    with open(TIMESTAMP_FILE_PATH, 'w') as file:
        file.write(timestamp)