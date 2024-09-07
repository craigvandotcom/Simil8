# Multi-Input to Tweet Bot

## Overview
This project is an advanced social media automation tool that integrates various input sources to generate tweets and threads. It currently supports:
- Monitoring specified Discord channels for new messages
- Fetching highlights from Readwise
- Generating tweet variations and threads using OpenAI's GPT model or Anthropic's Claude model
- Posting content to social media using Typefully

## Features
- Discord integration: Monitor specific channels for new messages
- Readwise integration: Fetch and process book highlights
- Tweet generation: Create tweet variations and threads from input text
- Typefully integration: Draft and schedule tweets for posting
- Periodic task execution: Process highlights and create tweet threads at regular intervals
- Logging: Comprehensive logging of message processing and API requests
- Web server: Flask-based web server for health checks and manual task triggering
- Environment-based configuration: Different settings for development and production

## Prerequisites
- Python 3.10+
- Discord Developer account
- Readwise account
- Typefully account
- OpenAI account
- Anthropic account
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
   DISCORD_WIF_THREAD_CHANNEL_ID=987654321
   DISCORD_BASIC_THREAD_CHANNEL_ID=456789123
   READWISE_TOKEN=your_readwise_token
   TYPEFULLY_API_KEY=your_typefully_api_key
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   DISCORD_ERROR_CHANNEL_ID=123456789
   DISCORD_HEALTH_CHECK_CHANNEL_ID=987654321
   REPLIT_DEPLOYMENT=false
   ```

3. Install dependencies:
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
- Adjust settings in `backend/app/config/user_settings.py`:
  - `READWISE_TASK_FREQUENCY`: Change how often the bot processes highlights and creates tweets
  - `AI_MODEL`: Choose between 'gpt-4' or 'claude-3-5-sonnet-20240620'
  - `TWEET_VARIATIONS_COUNT`: Set the number of tweet variations to generate
  - `MAX_THREAD_TWEETS`: Set the maximum number of tweets in a thread
- Modify the tweet generation prompts in `backend/app/config/prompts.py` to customize the output style and content

## API Endpoints
The Flask web server provides the following endpoints:
- `GET /`: Health check
- `POST /process-highlights`: Manually trigger highlight processing
- `POST /generate-tweets`: Generate tweet variations from provided text
- `POST /generate-threads`: Generate tweet threads from provided text
- `POST /run-frequent-task`: Manually trigger the periodic task

## Project Structure
- `backend/`: Main application code
  - `app/`: Core application modules
    - `config/`: Configuration files
    - `services/`: Service modules (Discord, Readwise, Typefully, etc.)
  - `routes/`: API route definitions
- `tests/`: Test files
- `frontend/`: (If applicable) Frontend code

## Testing
This project uses pytest for testing. To run the tests, follow these steps:

1. Ensure you have pytest and pytest-asyncio installed:
   ```bash
   poetry add pytest pytest-cov pytest-asyncio  # If using Poetry
   pip install pytest pytest-cov pytest-asyncio  # If using pip
   ```

2. Run all tests:
   ```bash
   pytest
   ```

3. Run tests with coverage report:
   ```bash
   pytest --cov=backend
   ```

4. Run a specific test file:
   ```bash
   pytest tests/test_routes.py
   ```

5. Run a specific test function:
   ```bash
   pytest tests/test_routes.py::test_health_check
   ```

### Discord Bot Tests
The project includes specific tests for the Discord bot functionality. These tests cover:

- Processing tweet content
- Processing thread content
- Handling messages in different channels
- Sending health status messages
- Sending error messages

To run the Discord bot tests specifically:
```bash
pytest tests/test_discord_bot.py
```

These tests use mocking to simulate Discord interactions and verify the bot's behavior without actually connecting to Discord servers.

The test files are located in the `tests/` directory. You can add more test files or modify existing ones as needed.

## Troubleshooting
- If you encounter missing environment variables, check your `.env` file and ensure all required variables are set
- For API-related issues, check the respective service documentation (Discord, Readwise, Typefully, OpenAI, Anthropic)
- Review the application logs for detailed error messages and stack traces

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
- Anthropic for Claude-based text generation
- Typefully for tweet scheduling and posting

## Contact
For support or to report issues, please open an issue on the GitHub repository.

## Changelog

### Version 0.1.1

- **Fixed**: Discord bot
- **Fixed**: Tweet variations flow
- **Fixed**: Thread flow
- **Fixed**: Readwise highlight task bug