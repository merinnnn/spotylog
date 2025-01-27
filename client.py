import requests
from .excel_utils import save_to_excel

class SpotifyClient:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://api.spotify.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def _get(self, endpoint, params=None):
        """Helper method for GET requests."""
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def search(self, query, type="track", limit=10):
        """Search for tracks, albums, artists, or playlists."""
        params = {
            "q": query,
            "type": type,
            "limit": limit,
        }
        return self._get("search", params=params)

    def get_user_playlists(self):
        """Get the current user's playlists."""
        return self._get("me/playlists")

    def create_playlist(self, user_id, name, description="", public=False):
        """Create a new playlist for the user."""
        data = {
            "name": name,
            "description": description,
            "public": public,
        }
        return self._post(f"users/{user_id}/playlists", data=data)

    def save_search_results_to_excel(self, query, type="track", limit=10, filename="search_results.xlsx"):
        """
        Search for items and save the results to an Excel file.
        
        Args:
            query (str): The search query.
            type (str): The type of item to search for (e.g., "track", "album").
            limit (int): The maximum number of results to return.
            filename (str): The name of the Excel file.
        """
        results = self.search(query, type=type, limit=limit)
        items = results.get(f"{type}s", {}).get("items", [])

        # Format data for Excel
        data = []
        for item in items:
            if type == "track":
                data.append({
                    "Name": item.get("name"),
                    "Artists": ", ".join(artist["name"] for artist in item.get("artists", [])),
                    "Album": item.get("album", {}).get("name"),
                    "Duration (ms)": item.get("duration_ms"),
                    "Popularity": item.get("popularity"),
                })
            elif type == "album":
                data.append({
                    "Name": item.get("name"),
                    "Artists": ", ".join(artist["name"] for artist in item.get("artists", [])),
                    "Release Date": item.get("release_date"),
                    "Total Tracks": item.get("total_tracks"),
                })
            elif type == "artist":
                data.append({
                    "Name": item.get("name"),
                    "Genres": ", ".join(item.get("genres", [])),
                    "Popularity": item.get("popularity"),
                })

        # Save to Excel
        save_to_excel(data, filename)

    def save_user_playlists_to_excel(self, filename="user_playlists.xlsx"):
        """
        Get the current user's playlists and save them to an Excel file.
        
        Args:
            filename (str): The name of the Excel file.
        """
        playlists = self.get_user_playlists().get("items", [])

        # Format data for Excel
        data = []
        for playlist in playlists:
            data.append({
                "Name": playlist.get("name"),
                "Description": playlist.get("description"),
                "Owner": playlist.get("owner", {}).get("display_name"),
                "Tracks": playlist.get("tracks", {}).get("total"),
                "Public": playlist.get("public"),
            })

        # Save to Excel
        save_to_excel(data, filename)