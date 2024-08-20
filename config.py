import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Log all environment variables (be careful with sensitive data in production)
logging.info("Environment variables:")
for key, value in os.environ.items():
    logging.info(f"{key}: {value}")

# Use .get() method with a default value for non-critical variables
READWISE_TOKEN = os.environ.get('READWISE_TOKEN')
TYPEFULLY_API_KEY = os.environ.get('TYPEFULLY_API_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Fetch the REPLIT_DEPLOYMENT value, convert to a string and handle common truthy values
replit_deployment_raw = os.environ.get('REPLIT_DEPLOYMENT', 'false').lower()
truthy_values = {'true', '1', 'yes', 'on'}
IS_PRODUCTION = replit_deployment_raw in truthy_values

# Log for debugging purposes
logging.info(f"REPLIT_DEPLOYMENT (raw): {replit_deployment_raw}")
logging.info(f"IS_PRODUCTION: {IS_PRODUCTION}")

# Personal Preferences
frequent_task_interval = int(os.environ.get('FREQUENT_TASK_INTERVAL', '1'))  # in minutes
DISCORD_TWEET_CHANNEL_ID = os.environ.get('DISCORD_TWEET_CHANNEL_ID')
DISCORD_THREAD_CHANNEL_ID = os.environ.get('DISCORD_THREAD_CHANNEL_ID')

def check_environment_variables():
    required_vars = [
        'DISCORD_BOT_TOKEN',
        'DISCORD_TWEET_CHANNEL_ID',
        'DISCORD_THREAD_CHANNEL_ID',
        'READWISE_TOKEN',
        'TYPEFULLY_API_KEY',
        'OPENAI_API_KEY'
    ]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    if missing_vars:
        for var in missing_vars:
            logging.error(f"Missing required environment variable: {var}")
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Call this function at the end of config.py
check_environment_variables()