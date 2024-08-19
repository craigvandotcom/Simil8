# standard library imports
import asyncio
import logging
import os
import threading
import time
from datetime import datetime

# third-party imports
import aiohttp
import requests
import schedule
from aiohttp import ClientSession

# local imports
from config import IS_PRODUCTION
from discord_bot import client as discord_client
from readwise_processor import process_highlights
from tweet_generator import create_highlight_thread
from typefully_api import create_typefully_draft
from web_server import start_server

# Environment
print(f"REPLIT_DEPLOYMENT (raw): {os.getenv('REPLIT_DEPLOYMENT')}")
print(f"IS_PRODUCTION: {IS_PRODUCTION}")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def run_frequent_task():
    logging.info(f"Running frequent task at {datetime.now()}")

    try:
        highlights = process_highlights()
        results = []

        for highlight in highlights:
            thread = create_highlight_thread(highlight)
            logging.info(f"Generated thread for highlight {highlight['id']}: {thread}")

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

def run_discord_bot():
    discord_client.run(os.getenv('DISCORD_BOT_TOKEN'))

if __name__ == "__main__":
    print(f"IS_PRODUCTION (final): {IS_PRODUCTION}")

    if IS_PRODUCTION:
        logging.info("Running in production mode")
        server_thread = threading.Thread(target=start_server)
        server_thread.start()

        discord_thread = threading.Thread(target=run_discord_bot)
        discord_thread.start()

        time.sleep(5)  # Wait for the servers to start
        logging.info("Scheduling the frequent task")
        schedule.every(frequent_task_interval).minutes.do(lambda: asyncio.run(run_frequent_task()))
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            logging.info("Shutting down...")
    else:
        logging.info("Running in development mode")
        server_thread = threading.Thread(target=start_server)
        server_thread.start()

        discord_thread = threading.Thread(target=run_discord_bot)
        discord_thread.start()

        time.sleep(5)  # Wait for the servers to start
        logging.info("Running task once for testing")
        asyncio.run(run_frequent_task())  # Run once for testing
        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            logging.info("Shutting down...")