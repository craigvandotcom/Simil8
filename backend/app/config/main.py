import os
import logging
from . import prompts
from .user_settings import *

class Config:
    # Add a class-level docstring explaining the purpose of this class
    """
    Configuration class for the application.
    Loads environment variables and sets up various configuration parameters.
    """

    # Add comments for each configuration variable
    READWISE_TOKEN = os.getenv('READWISE_TOKEN')  # API token for Readwise integration
    TYPEFULLY_API_KEY = os.getenv('TYPEFULLY_API_KEY')  # API key for Typefully integration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # API key for OpenAI services
    DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')  # Discord bot token
    DISCORD_TWEET_CHANNEL_ID = os.getenv('DISCORD_TWEET_CHANNEL_ID')  # Discord channel ID for tweets
    DISCORD_THREAD_CHANNEL_ID = os.getenv('DISCORD_THREAD_CHANNEL_ID')  # Discord channel ID for threads
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')  # API key for Anthropic services
    DISCORD_ERROR_CHANNEL_ID = os.getenv('DISCORD_ERROR_CHANNEL_ID')  # Discord channel ID for errors
    DISCORD_HEALTH_CHECK_CHANNEL_ID = os.getenv('DISCORD_HEALTH_CHECK_CHANNEL_ID')  # Discord channel ID for health checks

    replit_deployment_raw = os.getenv('REPLIT_DEPLOYMENT', 'false').lower()
    truthy_values = {'true', '1', 'yes', 'on'}
    IS_PRODUCTION = replit_deployment_raw in truthy_values

    PORT = int(os.getenv('PORT', 80))
    
    # Use READWISE_TASK_FREQUENCY from user_settings
    READWISE_TASK_FREQUENCY = READWISE_TASK_FREQUENCY

    # Load prompts from the prompts.py file
    PROMPTS = {
        SYSTEM_PROMPT_KEY: prompts.SYSTEM_PROMPT,
        TWEET_VARIATIONS_PROMPT_KEY: prompts.TWEET_VARIATIONS,
        BASIC_THREAD_PROMPT_KEY: prompts.BASIC_THREAD,
        WIF_THREAD_PROMPT_KEY: prompts.WIF_THREAD
    }

    # User settings
    TWEET_VARIATIONS_COUNT = TWEET_VARIATIONS_COUNT
    AI_MODEL = AI_MODEL
    MAX_THREAD_TWEETS = MAX_THREAD_TWEETS
    ENABLE_DISCORD_BOT = ENABLE_DISCORD_BOT
    ENABLE_READWISE_INTEGRATION = ENABLE_READWISE_INTEGRATION
    ENABLE_TYPEFULLY_INTEGRATION = ENABLE_TYPEFULLY_INTEGRATION
    THREAD_PROMPT_TYPE = THREAD_PROMPT_TYPE
    TWEET_VARIATIONS_PROMPT_TYPE = TWEET_VARIATIONS_PROMPT_TYPE

    @staticmethod
    def check_environment_variables():
        """
        Checks if all required environment variables are set.
        Raises an EnvironmentError if any required variable is missing.
        """
        required_vars = [
            'DISCORD_BOT_TOKEN', 'DISCORD_TWEET_CHANNEL_ID', 'DISCORD_THREAD_CHANNEL_ID',
            'READWISE_TOKEN', 'TYPEFULLY_API_KEY', 'OPENAI_API_KEY', 'ANTHROPIC_API_KEY',
            'DISCORD_ERROR_CHANNEL_ID', 'DISCORD_HEALTH_CHECK_CHANNEL_ID'
        ]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            error_msg = f"Missing required environment variables: {', '.join(missing_vars)}"
            logging.error(error_msg)
            raise EnvironmentError(error_msg)