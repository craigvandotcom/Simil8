# Multi-Input to Tweet Bot

## Overview

This project integrates various input sources to generate tweets and threads using a single API. Currently, it supports:
- Monitoring specified Discord channels for new messages.
- Fetching highlights from Readwise.

The generated content can then be posted to social media using Typefully.

## Features

- Monitor specified Discord channels for new messages.
- Fetch highlights from Readwise's export API.
- Send messages or highlights to an API endpoint to generate tweets and threads.
- Log message processing and API requests.
- Integrated with Typefully for drafting tweets.

## Prerequisites

- Python 3.10+
- Discord Developer account
- Readwise account
- Typefully account
- OpenAI account
- Docker (Optional, for containerized deployment)

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-repo/multi-input-to-tweet-bot.git
    cd multi-input-to-tweet-bot
    ```

2. **Set Up Environment**:
    - Create a `.env` file in the root directory and add the necessary environment variables:
    ```properties
    DISCORD_BOT_TOKEN=your_discord_bot_token
    TARGET_CHANNEL_IDS=123456789123456789,987654321987654321  # Replace with your actual channel IDs
    READWISE_TOKEN=your_readwise_token
    TYPEFULLY_API_KEY=your_typefully_api_key
    OPENAI_API_KEY=your_openai_api_key
    ```

3. **Install Dependencies**:
    - If using Poetry:
      ```bash
      poetry install
      ```
    - If using pip:
      ```bash
      pip install -r requirements.txt
      ```

## Setup Discord Bot

1. **Create a Discord Bot**:
    - Go to the [Discord Developer Portal](https://discord.com/developers/applications).
    - Create a new application.
    - Navigate to the **Bot** section and add a bot.
    - Enable `MESSAGE_CONTENT` intent in the Bot section. Save changes.
    - Copy the bot token and add it to your `.env` file as `DISCORD_BOT_TOKEN`.

2. **Invite the Bot to Your Server**:
    - Generate an OAuth2 URL with the necessary permissions and invite the bot to your server.
    - Example URL (Make sure to replace `YOUR_CLIENT_ID`):
      ```text
      https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=268446720&scope=bot%20applications.commands
      ```

## Setup Readwise Integration

1. **Get Your Readwise Token**:
    - Go to your Readwise account settings and find your API token.
    - Add it to the `.env` file as `READWISE_TOKEN`.

## Usage

To run the bot:

1. **Development Mode**:
    - Run the bot using Python:
      ```bash
      python main.py
      ```
    
    - Or, using Poetry:
      ```bash
      poetry run python main.py
      ```

2. **Production Mode**:
    - Ensure your `.env` file has `REPLIT_DEPLOYMENT = true`.
    - Deploy the bot following Replit's deployment instructions.

3. **Docker (Optional)**:
    - Build the Docker image:
      ```bash
      docker build -t multi-input-to-tweet-bot .
      ```
    - Run the Docker container:
      ```bash
      docker run --env-file .env -d multi-input-to-tweet-bot
      ```

## Endpoints

The Flask web server provides the following endpoints:

- `/`: Health check endpoint.
- `/process-highlights`: Processes Readwise highlights and generates drafts.
- `/generate-tweets`: Generates tweet variations from provided text.
- `/generate-threads`: Generates tweet threads from provided text.
- `/run-frequent-task`: Processes highlights and creates tweet threads periodically.

## Contributing

Contributions are welcome! Please create an issue or submit a pull request.

## License

This project is licensed under the MIT License.