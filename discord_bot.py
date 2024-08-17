import discord
import aiohttp
import os
import logging

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

TWEET_API_ENDPOINT = os.environ['TWEET_API_ENDPOINT']

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MyClient(discord.Client):
    async def on_ready(self):
        logging.info(f'Logged in as {self.user}')
        self.session = aiohttp.ClientSession()

    async def on_message(self, message):
        if message.channel.id in CHANNEL_IDS:
            logging.info(f'Received message: {message.content}')
            await self.send_to_api(message.content)

    async def send_to_api(self, message_content):
        async with self.session.post(TWEET_API_ENDPOINT, json={'text': message_content}) as response:
            if response.status == 200:
                logging.info(f"Message sent to API successfully: {message_content}")
            else:
                logging.error(f"Failed to send message to API: {message_content}")

    async def close(self):
        if hasattr(self, 'session'):
            await self.session.close()
        await super().close()

intents = discord.Intents.default()
intents.message_content = True  # Make sure this intent is enabled in the developer portal
client = MyClient(intents=intents)

if __name__ == '__main__':
    client.run(DISCORD_BOT_TOKEN)