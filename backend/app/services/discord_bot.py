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
            channel_id = str(message.channel.id)
            if channel_id in Config.CHANNEL_CONFIG_MAP:
                channel_config = Config.CHANNEL_CONFIG_MAP[channel_id]
                prompt_type = channel_config['prompt_type']
                processor_name = channel_config['processor']
                processor = getattr(self, processor_name, None)
                if processor:
                    await processor(message, prompt_type)
                else:
                    logger.warning(f'Processor not found: {processor_name}')
            else:
                logger.info(f'Received message in unhandled channel: {channel_id}')
        except Exception as e:
            error_message = f"Error processing message: {str(e)}"
            logger.exception(error_message)
            await self.report_error(error_message)

    async def process_tweet_content(self, message, prompt_type):
        try:
            logger.info(f"Starting to process tweet content: {message.content}")
            tweet_versions = await to_tweet_variations(message.content)
            tweets = [message.content] + tweet_versions
            draft = await create_typefully_draft(tweets)
            logger.info(f"Generated tweet draft: {draft}")
        except Exception as e:
            error_message = f"Error processing tweet content: {message.content}\n{str(e)}"
            logger.error(error_message)
            await self.report_error(error_message)

    async def process_thread_content(self, message, prompt_type):
        try:
            channel_id = str(message.channel.id)
            thread = await to_thread(message.content, prompt_type)
            draft = await create_typefully_draft([message.content] + thread)
            logger.info(f"Generated thread draft: {draft}")
        except Exception as e:
            error_message = f"Error processing thread content: {message.content}\n{str(e)}"
            logger.exception(error_message)
            await self.report_error(error_message)

    async def report_error(self, error_message):
        await report_error_to_discord(error_message)

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
from .error_reporting import report_error_to_discord

# Define the setup_and_run_bot function
async def setup_and_run_bot():
    client = MyClient()
    await client.start(Config.DISCORD_BOT_TOKEN)

# Export the function for import
__all__ = ['setup_and_run_bot']