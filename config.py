import os

READWISE_TOKEN = os.environ['READWISE_TOKEN']
TYPEFULLY_API_KEY = os.environ['TYPEFULLY_API_KEY']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

IS_PRODUCTION = os.getenv('REPLIT_DEPLOYMENT', '').lower() == 'true'