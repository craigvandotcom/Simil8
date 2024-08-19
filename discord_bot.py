import discord
import os
import logging
from tweet_generator import generate_tweet_variations
from typefully_api import create_typefully_draft

# Fetch environment variables
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_CHANNEL_IDS = os.getenv('DISCORD_CHANNEL_IDS')

# Validate environment variables
if not DISCORD_BOT_TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN environment variable is not set.")

if not DISCORD_CHANNEL_IDS:
    raise ValueError("DISCORD_CHANNEL_IDS environment variable is not set or empty.")

# Process and validate CHANNEL_IDS
try:
    CHANNEL_IDS = [int(id.strip()) for id in DISCORD_CHANNEL_IDS.split(',') if id.strip()]
except ValueError as e:
    raise ValueError("DISCORD_CHANNEL_IDS must be a comma-separated list of integers.") from e

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MyClient(discord.Client):
    async def on_ready(self):
        logging.info(f'Logged in as {self.user}')

    async def on_message(self, message):
        if message.channel.id in CHANNEL_IDS:
            logging.info(f'Received message: {message.content}')
            await self.process_message_content(message.content)

    async def process_message_content(self, message_content):
        try:
            tweet_versions = generate_tweet_variations(message_content)
            draft = create_typefully_draft(tweet_versions)
            logging.info(f"Generated draft: {draft}")
        except Exception as e:
            logging.error(f"Error processing message content: {message_content}", exc_info=True)

intents = discord.Intents.default()
intents.message_content = True  # Make sure this intent is enabled in the developer portal
client = MyClient(intents=intents)

if __name__ == '__main__':
    client.run(DISCORD_BOT_TOKEN)