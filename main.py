import asyncio
import logging
from backend.app import create_app
from backend.app.config import Config
from backend.app.services.discord_bot import setup_and_run_bot, report_error_to_discord
from backend.app.services.readwise_processor import run_frequent_task

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = create_app()

async def main():
    logging.info("Starting main function...")
    tasks = [run_frequent_task()]

    if Config.ENABLE_DISCORD_BOT:
        tasks.append(setup_and_run_bot())

    if Config.IS_PRODUCTION:
        logging.info("Running in production mode")
        # In production, run Flask in a separate thread
        from threading import Thread
        flask_thread = Thread(target=lambda: app.run(host='0.0.0.0', port=int(Config.PORT)))
        flask_thread.start()
    else:
        logging.info("Running in development mode")
        # In development, run Flask as an asyncio task
        tasks.append(app.run_task(host='0.0.0.0', port=int(Config.PORT)))

    try:
        await asyncio.gather(*tasks)
    except Exception as e:
        error_message = f"Error in main function: {str(e)}"
        logging.error(error_message, exc_info=True)
        try:
            await report_error_to_discord(error_message)
        except Exception as discord_error:
            logging.error(f"Failed to report error to Discord: {str(discord_error)}", exc_info=True)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}", exc_info=True)