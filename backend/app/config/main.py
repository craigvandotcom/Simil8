import os
import logging
from . import prompts
from .user_settings import *

class Config:
    READWISE_TOKEN = os.getenv('READWISE_TOKEN')
    TYPEFULLY_API_KEY = os.getenv('TYPEFULLY_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    DISCORD_TWEET_CHANNEL_ID = os.getenv('DISCORD_TWEET_CHANNEL_ID')
    DISCORD_THREAD_CHANNEL_ID = os.getenv('DISCORD_THREAD_CHANNEL_ID')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    DISCORD_ERROR_CHANNEL_ID = os.getenv('DISCORD_ERROR_CHANNEL_ID')
    DISCORD_HEALTH_CHECK_CHANNEL_ID = os.getenv('DISCORD_HEALTH_CHECK_CHANNEL_ID')

    replit_deployment_raw = os.getenv('REPLIT_DEPLOYMENT', 'false').lower()
    truthy_values = {'true', '1', 'yes', 'on'}
    IS_PRODUCTION = replit_deployment_raw in truthy_values

    PORT = os.getenv('PORT', 80)
    FREQUENT_TASK_INTERVAL = int(os.getenv('FREQUENT_TASK_INTERVAL', '1'))  # in minutes

    # Load prompts from the prompts.py file
    PROMPTS = {
        "system_prompt": prompts.SYSTEM_PROMPT,
        "tweet_variations": prompts.TWEET_VARIATIONS,
        "thread": prompts.THREAD
    }

    # User settings
    TWEET_VARIATIONS_COUNT = TWEET_VARIATIONS_COUNT
    AI_MODEL = AI_MODEL
    READWISE_TASK_FREQUENCY = READWISE_TASK_FREQUENCY or FREQUENT_TASK_INTERVAL
    MAX_THREAD_TWEETS = MAX_THREAD_TWEETS
    ENABLE_DISCORD_BOT = ENABLE_DISCORD_BOT
    ENABLE_READWISE_INTEGRATION = ENABLE_READWISE_INTEGRATION
    ENABLE_TYPEFULLY_INTEGRATION = ENABLE_TYPEFULLY_INTEGRATION

    @staticmethod
    def check_environment_variables():
        required_vars = [
            'DISCORD_BOT_TOKEN',
            'DISCORD_TWEET_CHANNEL_ID',
            'DISCORD_THREAD_CHANNEL_ID',
            'READWISE_TOKEN',
            'TYPEFULLY_API_KEY',
            'OPENAI_API_KEY',
            'ANTHROPIC_API_KEY',
            'DISCORD_ERROR_CHANNEL_ID',
            'DISCORD_HEALTH_CHECK_CHANNEL_ID'
        ]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            for var in missing_vars:
                logging.error(f"Missing required environment variable: {var}")
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")