# User-configurable settings

# AI model to use for content generation ('gpt-4', 'claude-3-5-sonnet-20240620')
AI_MODEL = 'claude-3-5-sonnet-20240620'

# Frequency of the Readwise task in minutes
READWISE_TASK_FREQUENCY = 1  # Changed from 60 to 1

# Maximum number of tweets in a thread
MAX_THREAD_TWEETS = 7

# Enable or disable specific features
ENABLE_DISCORD_BOT = True
ENABLE_READWISE_INTEGRATION = True
ENABLE_TYPEFULLY_INTEGRATION = True

# Channel to prompt type and processor mapping
CHANNEL_CONFIG_MAP = {
    'DISCORD_TWEET_CHANNEL_ID': {
        'prompt_type': 'TWEET_VARIATIONS',
        'processor': 'process_tweet_content'
    },
    'DISCORD_WIF_THREAD_CHANNEL_ID': {
        'prompt_type': 'WIF_THREAD',
        'processor': 'process_thread_content'
    },
    'DISCORD_BASIC_THREAD_CHANNEL_ID': {
        'prompt_type': 'BASIC_THREAD',
        'processor': 'process_thread_content'
    },
    # Add more channel mappings as needed
}

# Prompt keys
SYSTEM_PROMPT_KEY = 'SYSTEM_PROMPT'
TWEET_VARIATIONS_PROMPT_KEY = 'TWEET_VARIATIONS'
BASIC_THREAD_PROMPT_KEY = 'BASIC_THREAD'
WIF_THREAD_PROMPT_KEY = 'WIF_THREAD'

# Add any other user-configurable settings here