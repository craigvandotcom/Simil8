from ..logger import get_logger

logger = get_logger(__name__)

async def report_error(error_message: str):
    """
    Placeholder function for error reporting.
    This will be implemented later to actually send errors to Discord.
    """
    logger.error(f"Error reported: {error_message}")

# This function will be implemented in discord_bot.py
report_error_to_discord = None

def set_error_reporter(reporter_func):
    global report_error_to_discord
    report_error_to_discord = reporter_func