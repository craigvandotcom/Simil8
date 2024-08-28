from .main import Config

class TestConfig(Config):
    TESTING = True
    IS_PRODUCTION = False
    # Add other test-specific configurations here
    DISCORD_BOT_TOKEN = 'test_token'
    READWISE_TOKEN = 'test_token'
    TYPEFULLY_API_KEY = 'test_key'
    OPENAI_API_KEY = 'test_key'