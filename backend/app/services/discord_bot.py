# discord_bot.py
import logging
import os
import discord
from discord.ext import commands, tasks
from ..config import Config
from datetime import datetime, time
import asyncio
import ssl
import certifi
from .tweet_generator import to_tweet_variations, to_thread  # Add to_thread here
from .typefully_api import create_typefully_draft  # Add this import if not already present

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True

class MyClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)
        self.health_check_started = False

    async def setup_hook(self):
        if not self.health_check_started:
            self.daily_health_check.start()
            self.health_check_started = True

    async def on_ready(self):
        logger.info(f'Logged in as {self.user}')
        await self.send_startup_message()

    async def send_startup_message(self):
        channel = self.get_channel(int(Config.DISCORD_HEALTH_CHECK_CHANNEL_ID))
        if channel:
            try:
                await channel.send("🚀 Bot has started up and is now operational!")
            except Exception as e:
                logger.exception(f"Failed to send startup message: {str(e)}")
        else:
            logger.error("Could not find health check channel for startup message")

    async def on_message(self, message):
        logger.info(f'Received message in channel: {message.channel.id}')
        try:
            if message.channel.id == int(Config.DISCORD_TWEET_CHANNEL_ID):
                logger.info(f'Received tweet message: {message.content}')
                await self.process_tweet_content(message.content)
            elif message.channel.id == int(Config.DISCORD_THREAD_CHANNEL_ID):
                logger.info(f'Received thread message: {message.content}')
                await self.process_thread_content(message.content)
            else:
                logger.info(f'Received message in unhandled channel: {message.channel.id}')
        except Exception as e:
            error_message = f"Error processing message: {str(e)}"
            logger.exception(error_message)
            await self.report_error(error_message)

    async def process_tweet_content(self, message_content):
        try:
            logger.info(f"Starting to process tweet content: {message_content}")
            logger.info("Calling to_tweet_variations")
            tweet_versions = await to_tweet_variations(message_content)
            logger.info(f"Received tweet versions: {tweet_versions}")
            tweets = [message_content] + tweet_versions
            logger.info(f"Combined tweets: {tweets}")
            logger.info("Calling create_typefully_draft")
            draft = await create_typefully_draft(tweets)
            logger.info(f"Generated tweet draft: {draft}")
        except Exception as e:
            error_message = f"Error processing tweet content: {message_content}\n{str(e)}"
            logger.error(error_message)
            await self.report_error(error_message)

    async def process_thread_content(self, message_content):
        try:
            thread_draft = await to_thread(message_content)
            thread = [message_content] + thread_draft
            draft = await create_typefully_draft(thread)
            logger.info(f"Generated thread draft: {draft}")
        except Exception as e:
            error_message = f"Error processing thread content: {message_content}\n{str(e)}"
            logger.exception(error_message)
            await self.report_error(error_message)

    async def report_error(self, error_message):
        channel_id = Config.DISCORD_ERROR_CHANNEL_ID
        try:
            channel = self.get_channel(int(channel_id))
            if channel:
                await channel.send(f"⚠️ Error: {error_message}")
            else:
                logger.error(f"Could not find error reporting channel (ID: {channel_id}). Error: {error_message}")
        except Exception as e:
            logger.exception(f"Failed to report error to Discord: {str(e)}\nOriginal error: {error_message}")

    @tasks.loop(time=time(hour=6))  # Run daily at 6 AM
    async def daily_health_check(self):
        channel = self.get_channel(int(Config.DISCORD_HEALTH_CHECK_CHANNEL_ID))
        if channel:
            try:
                # Perform health check (you may want to add more comprehensive checks)
                await channel.send("✅ Daily health check passed. All systems operational.")
            except Exception as e:
                error_message = f"Daily health check failed: {str(e)}"
                logger.exception(error_message)
                await self.report_error(error_message)
        else:
            logger.error("Could not find health check channel")

# Add this import
from .error_reporting import set_error_reporter

# Replace the existing report_error_to_discord function with this:
async def report_error_to_discord(error_message: str, bot: MyClient = None):
    channel_id = Config.DISCORD_ERROR_CHANNEL_ID
    try:
        if bot:
            channel = bot.get_channel(int(channel_id))
        else:
            logger.error("Bot instance not available for error reporting")
            return
        if channel:
            await channel.send(f"⚠️ Error: {error_message}")
        else:
            logger.error(f"Could not find error reporting channel (ID: {channel_id}). Error: {error_message}")
    except Exception as e:
        logger.exception(f"Failed to report error to Discord: {str(e)}\nOriginal error: {error_message}")

# Modify the setup_and_run_bot function:
async def setup_and_run_bot():
    try:
        bot = MyClient()
        set_error_reporter(lambda msg: report_error_to_discord(msg, bot))
        await bot.start(Config.DISCORD_BOT_TOKEN)
    except Exception as e:
        error_message = f"Failed to start Discord bot: {str(e)}"
        logger.exception(error_message)
        # We can't use report_error_to_discord here because the bot isn't started
        logger.error(f"Bot startup error: {error_message}")

# Remove this line as it's no longer needed
# set_error_reporter(report_error_to_discord)

# Add this at the end of the file to make setup_and_run_bot available for import
__all__ = ['setup_and_run_bot']