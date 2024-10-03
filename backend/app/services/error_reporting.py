import aiohttp
import asyncio
from ..config import Config
from ..logger import get_logger

logger = get_logger(__name__)

async def report_error_to_discord(error_message: str):
    webhook_url = Config.DISCORD_ERROR_WEBHOOK_URL
    if not webhook_url:
        logger.error("Discord error webhook URL is not set")
        return

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(webhook_url, json={"content": f"Error: {error_message}"}) as response:
                if response.status != 204:
                    logger.error(f"Failed to send error to Discord. Status: {response.status}")
        except Exception as e:
            logger.error(f"Exception while sending error to Discord: {str(e)}")

def report_error_to_discord_sync(error_message: str):
    asyncio.run(report_error_to_discord(error_message))

# This can be used to set a custom error reporter if needed
# def set_error_reporter(reporter_func):
#     global report_error_to_discord
#     report_error_to_discord = reporter_func

# Initialize with the default implementation
# set_error_reporter(report_error_to_discord)