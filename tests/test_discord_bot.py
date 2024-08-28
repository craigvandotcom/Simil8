import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from backend.app.services.discord_bot import MyClient
from backend.app.config import Config

class TestDiscordBot(unittest.TestCase):
    def setUp(self):
        self.bot = MyClient()
        self.bot.get_channel = MagicMock()

    @patch('backend.app.services.discord_bot.to_tweet_variations')
    @patch('backend.app.services.discord_bot.create_typefully_draft')
    async def test_process_tweet_content(self, mock_create_typefully_draft, mock_to_tweet_variations):
        # Mock the necessary functions and their return values
        mock_to_tweet_variations.return_value = ["Tweet variation 1", "Tweet variation 2"]
        mock_create_typefully_draft.return_value = {"id": "draft_id", "share_url": "https://typefully.com/draft/123"}

        # Test message content
        message_content = "Test tweet content"

        # Call the method
        await self.bot.process_tweet_content(message_content)

        # Assert that the mocked functions were called with the correct arguments
        mock_to_tweet_variations.assert_called_once_with(message_content)
        mock_create_typefully_draft.assert_called_once_with([message_content, "Tweet variation 1", "Tweet variation 2"])

    @patch('backend.app.services.discord_bot.to_thread')
    @patch('backend.app.services.discord_bot.create_typefully_draft')
    async def test_process_thread_content(self, mock_create_typefully_draft, mock_to_thread):
        # Mock the necessary functions and their return values
        mock_to_thread.return_value = ["Thread tweet 1", "Thread tweet 2"]
        mock_create_typefully_draft.return_value = {"id": "draft_id", "share_url": "https://typefully.com/draft/456"}

        # Test message content
        message_content = "Test thread content"

        # Call the method
        await self.bot.process_thread_content(message_content)

        # Assert that the mocked functions were called with the correct arguments
        mock_to_thread.assert_called_once_with(message_content)
        mock_create_typefully_draft.assert_called_once_with([message_content, "Thread tweet 1", "Thread tweet 2"])

    async def test_on_message(self):
        # Create a mock message
        mock_message = AsyncMock()
        mock_message.content = "Test message"

        # Test tweet channel
        mock_message.channel.id = int(Config.DISCORD_TWEET_CHANNEL_ID)
        self.bot.process_tweet_content = AsyncMock()
        await self.bot.on_message(mock_message)
        self.bot.process_tweet_content.assert_called_once_with("Test message")

        # Test thread channel
        mock_message.channel.id = int(Config.DISCORD_THREAD_CHANNEL_ID)
        self.bot.process_thread_content = AsyncMock()
        await self.bot.on_message(mock_message)
        self.bot.process_thread_content.assert_called_once_with("Test message")

        # Test unhandled channel
        mock_message.channel.id = 999999  # Some other channel ID
        await self.bot.on_message(mock_message)
        # Assert that neither process_tweet_content nor process_thread_content were called
        self.bot.process_tweet_content.assert_called_once()  # Only called in the first test
        self.bot.process_thread_content.assert_called_once()  # Only called in the second test

    @patch('backend.app.services.discord_bot.MyClient.get_channel')
    async def test_send_health_status_message(self, mock_get_channel):
        # Mock the channel
        mock_channel = AsyncMock()
        mock_get_channel.return_value = mock_channel

        # Call the daily health check method
        await self.bot.daily_health_check()

        # Assert that the health status message was sent
        mock_channel.send.assert_called_once_with("✅ Daily health check passed. All systems operational.")

    @patch('backend.app.services.discord_bot.MyClient.get_channel')
    async def test_send_error_message(self, mock_get_channel):
        # Mock the channel
        mock_channel = AsyncMock()
        mock_get_channel.return_value = mock_channel

        # Call the report_error method
        error_message = "Test error message"
        await self.bot.report_error(error_message)

        # Assert that the error message was sent
        mock_channel.send.assert_called_once_with(f"⚠️ Error: {error_message}")

if __name__ == '__main__':
    unittest.main()