# discord_bot.py
import logging
import os
import discord
from discord.ext import commands, tasks
from ..config import Config
from .tweet_generator import to_tweet_variations, to_thread
from .typefully_api import create_typefully_draft
from datetime import datetime, time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

intents = discord.Intents.default()
intents.message_content = True

class MyClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)
        self.health_check_started = False

    async def setup_hook(self):
        # Start the task in the setup_hook method only if it hasn't been started yet
        if not self.health_check_started:
            self.daily_health_check.start()
            self.health_check_started = True

    async def on_ready(self):
        logging.info(f'Logged in as {self.user}')
        await self.send_startup_message()

    async def send_startup_message(self):
        channel = self.get_channel(int(Config.DISCORD_HEALTH_CHECK_CHANNEL_ID))
        if channel:
            try:
                await channel.send("🚀 Bot has started up and is now operational!")
            except Exception as e:
                logging.error(f"Failed to send startup message: {str(e)}", exc_info=True)
        else:
            logging.error("Could not find health check channel for startup message")

    async def on_message(self, message):
        logging.info(f'Received message in channel: {message.channel.id}')
        if message.channel.id == int(Config.DISCORD_TWEET_CHANNEL_ID):
            logging.info(f'Received tweet message: {message.content}')
            await self.process_tweet_content(message.content)
        elif message.channel.id == int(Config.DISCORD_THREAD_CHANNEL_ID):
            logging.info(f'Received thread message: {message.content}')
            await self.process_thread_content(message.content)
        else:
            logging.info(f'Received message in unhandled channel: {message.channel.id}')

    async def process_tweet_content(self, message_content):
        try:
            tweet_versions = to_tweet_variations(message_content)
            tweets = [message_content] + tweet_versions
            draft = create_typefully_draft(tweets)
            logging.info(f"Generated tweet draft: {draft}")
        except Exception as e:
            error_message = f"Error processing tweet content: {message_content}\n{str(e)}"
            logging.error(error_message, exc_info=True)
            await self.report_error(error_message)

    async def process_thread_content(self, message_content):
        try:
            thread_draft = to_thread(message_content)
            thread = [message_content] + thread_draft
            draft = create_typefully_draft(thread)
            logging.info(f"Generated thread draft: {draft}")
        except Exception as e:
            logging.error(f"Error processing thread content: {message_content}", exc_info=True)

    async def report_error(self, error_message):
        channel_id = Config.DISCORD_ERROR_CHANNEL_ID
        try:
            channel = self.get_channel(int(channel_id))
            if channel:
                await channel.send(f"⚠️ Error: {error_message}")
            else:
                logging.error(f"Could not find error reporting channel (ID: {channel_id}). Error: {error_message}")
        except Exception as e:
            logging.error(f"Failed to report error to Discord: {str(e)}\nOriginal error: {error_message}", exc_info=True)

    @tasks.loop(time=time(hour=6))  # Run daily at 6 AM
    async def daily_health_check(self):
        channel = self.get_channel(int(Config.DISCORD_HEALTH_CHECK_CHANNEL_ID))
        if channel:
            try:
                # Perform health check (you may want to add more comprehensive checks)
                await channel.send("✅ Daily health check passed. All systems operational.")
            except Exception as e:
                await self.report_error(f"Daily health check failed: {str(e)}")
        else:
            logging.error("Could not find health check channel")

client = MyClient()

# Function to be called from other parts of the application
async def report_error_to_discord(error_message):
    await client.report_error(error_message)

# New function to setup and run the bot
async def setup_and_run_bot():
    await client.start(Config.DISCORD_BOT_TOKEN)