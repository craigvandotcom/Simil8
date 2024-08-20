# standard library imports
import asyncio
import logging
import os
import threading
import time
from datetime import datetime

# third-party imports
import schedule
from flask import Flask

# local imports
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
        return results
    except Exception as e:
        logging.error(f"Error in frequent task: {str(e)}", exc_info=True)
        raise

def run_discord_bot():
    discord_client.run(os.getenv('DISCORD_BOT_TOKEN'))

if __name__ == "__main__":
    try:
        check_environment_variables()
        logging.info(f"IS_PRODUCTION: {IS_PRODUCTION}")

        if IS_PRODUCTION:
            logging.info("Running in production mode")

            # Start Discord bot in a separate thread
            discord_thread = threading.Thread(target=run_discord_bot)
            discord_thread.start()

            # Start Flask server in a separate thread
            flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=80))
            flask_thread.start()

            time.sleep(5)  # Wait for the Discord bot to start
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

            # Start Discord bot in a separate thread
            discord_thread = threading.Thread(target=run_discord_bot)
            discord_thread.start()

            time.sleep(5)  # Wait for the Discord bot to start
            logging.info("Running task once for testing")
            asyncio.run(run_frequent_task())  # Run once for testing
            try:
                while True:
                    time.sleep(60)
            except KeyboardInterrupt:
                logging.info("Shutting down...")
    except EnvironmentError as e:
        logging.error(f"Configuration error: {str(e)}")
        exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}", exc_info=True)
        exit(1)