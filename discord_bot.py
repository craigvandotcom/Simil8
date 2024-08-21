# discord_bot.py
import logging
import os

import discord
from discord.ext import commands

from config import DISCORD_TWEET_CHANNEL_ID, DISCORD_THREAD_CHANNEL_ID
from tweet_generator import generate_tweet_variations, generate_thread
from typefully_api import create_typefully_draft

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

intents = discord.Intents.default()
intents.message_content = True

class MyClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)

    async def on_ready(self):
        logging.info(f'Logged in as {self.user}')

    async def on_message(self, message):
        logging.info(f'Received message in channel: {message.channel.id}')
        if message.channel.id == int(DISCORD_TWEET_CHANNEL_ID):
            logging.info(f'Received tweet message: {message.content}')
            await self.process_tweet_content(message.content)
        elif message.channel.id == int(DISCORD_THREAD_CHANNEL_ID):
            logging.info(f'Received thread message: {message.content}')
            await self.process_thread_content(message.content)

    async def process_tweet_content(self, message_content):
        try:
            tweet_versions = generate_tweet_variations(message_content)
            tweets = [message_content] + tweet_versions
            draft = create_typefully_draft(tweets)
            logging.info(f"Generated tweet draft: {draft}")
        except Exception as e:
            logging.error(f"Error processing tweet content: {message_content}", exc_info=True)

    async def process_thread_content(self, message_content):
        try:
            thread = generate_thread(message_content)
            draft = create_typefully_draft(thread)
            logging.info(f"Generated thread draft: {draft}")
        except Exception as e:
            logging.error(f"Error processing thread content: {message_content}", exc_info=True)

client = MyClient()

# Note: We're not calling client.run() here. This will be handled in main.py