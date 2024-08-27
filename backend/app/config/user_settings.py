# User-configurable settings

# Number of tweet variations to generate
TWEET_VARIATIONS_COUNT = 6

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

# Prompt selection
SYSTEM_PROMPT_KEY = 'system_prompt'
TWEET_VARIATIONS_PROMPT_KEY = 'tweet_variations'
BASIC_THREAD_PROMPT_KEY = 'basic_thread'
WIF_THREAD_PROMPT_KEY = 'wif_thread'

# Prompt type selection
THREAD_PROMPT_TYPE = WIF_THREAD_PROMPT_KEY  # or BASIC_THREAD_PROMPT_KEY
TWEET_VARIATIONS_PROMPT_TYPE = TWEET_VARIATIONS_PROMPT_KEY  # Default to standard tweet variations

# Add any other user-configurable settings here