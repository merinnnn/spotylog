import aiohttp
import asyncio

class AsyncSpotifyClient:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://api.spotify.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    async def _get(self, endpoint, params=None):
        """Async helper method for GET requests."""
        url = f"{self.base_url}/{endpoint}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers, params=params) as response:
                response.raise_for_status()
                return await response.json()

    async def search(self, query, type="track", limit=10):
        """Async search for tracks, albums, artists, or playlists."""
        params = {
            "q": query,
            "type": type,
            "limit": limit,
        }
        return await self._get("search", params=params)