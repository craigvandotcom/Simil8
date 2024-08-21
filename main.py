import asyncio
import logging
import os
from datetime import datetime
import threading

from flask import Flask

from config import IS_PRODUCTION, frequent_task_interval, check_environment_variables
from discord_bot import client as discord_client
from readwise_processor import process_highlights
from tweet_generator import create_highlight_thread
from typefully_api import create_typefully_draft

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Flask app initialization
app = Flask(__name__)

@app.route('/')
def health_check():
    return 'Health check passed', 200

async def run_frequent_task():
    while True:
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

        # Wait for the next interval
        await asyncio.sleep(frequent_task_interval * 60)

async def run_discord_bot():
    logging.info("Starting Discord bot...")
    try:
        await discord_client.start(os.getenv('DISCORD_BOT_TOKEN'))
    except Exception as e:
        logging.error(f"Error starting Discord bot: {str(e)}", exc_info=True)

async def run_flask():
    logging.info("Starting Flask app...")
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 80)))

async def main():
    logging.info("Starting main function...")
    tasks = [run_frequent_task(), run_discord_bot()]

    if IS_PRODUCTION:
        logging.info("Running in production mode")
        # In production, run Flask in a separate thread
        flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.getenv('PORT', 80))))
        flask_thread.start()
    else:
        logging.info("Running in development mode")
        # In development, run Flask as an asyncio task
        tasks.append(run_flask())

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        logging.info("Script started")
        check_environment_variables()
        asyncio.run(main())
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}", exc_info=True)
        exit(1)