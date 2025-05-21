import pytest
from motortwit.main import init

@pytest.fixture
async def app():
    """Create and return a test application instance."""
    app, _, _ = await init()
    return app


@pytest.fixture
async def client(aiohttp_client, app):
    """Create and return a test client."""
    return await aiohttp_client(app)

