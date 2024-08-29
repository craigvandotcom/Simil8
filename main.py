import asyncio
from backend.app import create_app
from backend.app.config import Config
from backend.app.services.discord_bot import setup_and_run_bot
from backend.app.services.error_reporting import report_error_to_discord
from backend.app.services.readwise_processor import run_frequent_task
from backend.app.logger import get_logger
from threading import Thread
import os

# Configure logging
logger = get_logger(__name__)

app = create_app()

def run_flask():
    """Run Flask application"""
    app.run(host='0.0.0.0', port=int(Config.PORT), debug=not Config.IS_PRODUCTION)

async def main():
    """
    Main asynchronous function to run the application.
    Sets up and runs the Discord bot, frequent tasks, and Flask server.
    """
    logger.info("Starting main function", extra={"action": "start_main"})
    tasks = [run_frequent_task()]

    if Config.ENABLE_DISCORD_BOT:
        tasks.append(setup_and_run_bot())

    # Run Flask in a separate process
    if os.fork() == 0:  # Child process
        run_flask()
        os._exit(0)
    else:  # Parent process
        try:
            await asyncio.gather(*tasks)
        except Exception as e:
            error_message = f"Error in main function: {str(e)}"
            logger.exception(error_message)
            await report_error_to_discord(error_message)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.exception(f"Fatal error: {str(e)}")
        asyncio.run(report_error_to_discord(f"Fatal error: {str(e)}"))