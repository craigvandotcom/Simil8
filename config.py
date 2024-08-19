import os

READWISE_TOKEN = os.getenv('READWISE_TOKEN')
TYPEFULLY_API_KEY = os.getenv('TYPEFULLY_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Fetch the REPLIT_DEPLOYMENT value, convert to a string and handle common truthy values
replit_deployment_raw = os.getenv('REPLIT_DEPLOYMENT', '').lower()
truthy_values = {'true', '1', 'yes'}
IS_PRODUCTION = replit_deployment_raw in truthy_values

# Log for debugging purposes
print(f"REPLIT_DEPLOYMENT (raw): {replit_deployment_raw}")
print(f"IS_PRODUCTION: {IS_PRODUCTION}")

# Personal Preferences
frequent_task_interval = 1  # in minutes