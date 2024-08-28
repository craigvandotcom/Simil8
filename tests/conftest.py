import pytest
import pytest_asyncio
from backend.app import create_app
from backend.app.config.test_config import TestConfig

@pytest_asyncio.fixture
async def app():
    app = create_app(TestConfig)
    yield app

@pytest_asyncio.fixture
async def client(app):
    return app.test_client()

# Add this new fixture for Discord bot tests
@pytest_asyncio.fixture
async def discord_bot():
    from backend.app.services.discord_bot import MyClient
    return MyClient()