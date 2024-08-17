import os
import schedule
import time
from datetime import datetime
from config import IS_PRODUCTION
from web_server import start_server
import threading
import requests
import logging
from discord_bot import client as discord_client

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_task():
    logging.info(f"Running task at {datetime.now()}")
    try:
        response = requests.post('http://localhost:8080/run-hourly-task')
        response.raise_for_status()
        result = response.json()
        logging.info(f"Task completed. Results: {result}")
    except requests.RequestException as e:
        logging.error(f"Error calling /run-hourly-task endpoint: {str(e)}", exc_info=True)
    except Exception as e:
        logging.error(f"Unexpected error in task: {str(e)}", exc_info=True)

def run_discord_bot():
    discord_client.run(os.getenv('DISCORD_BOT_TOKEN'))

if __name__ == "__main__":
    if IS_PRODUCTION:
        logging.info("Running in production mode")
        server_thread = threading.Thread(target=start_server)
        server_thread.start()

        discord_thread = threading.Thread(target=run_discord_bot)
        discord_thread.start()

        time.sleep(5)  # Wait for the servers to start
        schedule.every(15).minutes.do(run_task)
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
        run_task()  # Run once for testing
        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            logging.info("Shutting down...")