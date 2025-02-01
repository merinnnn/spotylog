import sys
import os

# Add the root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import AsyncMock, patch
from spotylog.async_client import AsyncSpotifyClient

# Fixture to create a mock AsyncSpotifyClient instance
@pytest.fixture
def mock_async_client():
    return AsyncSpotifyClient("dummy_access_token")

# Test async search functionality
@pytest.mark.asyncio
async def test_async_search(mock_async_client):
    with patch("aiohttp.ClientSession.get") as mock_get:
        # Mock the API response
        mock_get.return_value.__aenter__.return_value.json = AsyncMock(return_value={
            "tracks": {
                "items": [
                    {"name": "Believer", "artists": [{"name": "Imagine Dragons"}], "album": {"name": "Evolve"}}
                ]
            }
        })
        mock_get.return_value.__aenter__.return_value.raise_for_status = AsyncMock(return_value=None)

        # Call the async search method
        results = await mock_async_client.search("Imagine Dragons")

        # Assert the results
        assert "tracks" in results
        assert results["tracks"]["items"][0]["name"] == "Believer"