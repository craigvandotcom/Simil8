# Multi-Input to Tweet Bot
## Overview
This project is an advanced social media automation tool that integrates various input sources to generate tweets and threads. It currently supports:
- Monitoring specified Discord channels for new messages
- Fetching highlights from Readwise
- Generating tweet variations and threads using OpenAI's GPT model
- Posting content to social media using Typefully

## Features
- Discord integration: Monitor specific channels for new messages
- Readwise integration: Fetch and process book highlights
- Tweet generation: Create tweet variations and threads from input text
- Typefully integration: Draft and schedule tweets for posting
- Periodic task execution: Process highlights and create tweet threads at regular intervals
- Logging: Comprehensive logging of message processing and API requests
- Web server: Flask-based web server for health checks and manual task triggering

## Prerequisites
- Python 3.10+
- Discord Developer account
- Readwise account
- Typefully account
- OpenAI account
- Docker (optional, for containerized deployment)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/multi-input-to-tweet-bot.git
   cd multi-input-to-tweet-bot
   ```

2. Set up the environment:
   Create a `.env` file in the root directory with the following variables:
   ```env
   DISCORD_BOT_TOKEN=your_discord_bot_token
   DISCORD_TWEET_CHANNEL_ID=123456789
   DISCORD_THREAD_CHANNEL_ID=987654321
   READWISE_TOKEN=your_readwise_token
   TYPEFULLY_API_KEY=your_typefully_api_key
   OPENAI_API_KEY=your_openai_api_key
   REPLIT_DEPLOYMENT=true
   ```
4. Install dependencies:
   Using Poetry (recommended):
   ```bash
   poetry install
   ```
   Using pip:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
### Development Mode
Run the bot using Python:
   ```bash
   python main.py
   ```
Or, using Poetry:
   ```bash
   poetry run python main.py
   ```
### Production Mode
Set `REPLIT_DEPLOYMENT=true` in your `.env` file.
Deploy the bot following Replit's deployment instructions.

### Docker (Optional)
Build the Docker image:
   ```bash
   docker build -t multi-input-to-tweet-bot .
   ```
Run the Docker container:
   ```bash
   docker run --env-file .env -d multi-input-to-tweet-bot
   ```

## Configuration
Adjust the `frequent_task_interval` in `config.py` to change how often the bot processes highlights and creates tweets.
Modify the tweet generation prompts in `prompts.json` to customize the output style and content.

## API Endpoints
The Flask web server provides the following endpoints:
- `GET /`: Health check
- `POST /process-highlights`: Manually trigger highlight processing
- `POST /generate-tweets`: Generate tweet variations from provided text
- `POST /generate-threads`: Generate tweet threads from provided text
- `POST /run-frequent-task`: Manually trigger the periodic task

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a pull request

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements
- Discord.py for Discord integration
- Readwise for highlight retrieval
- OpenAI for GPT-based text generation
- Typefully for tweet scheduling and posting