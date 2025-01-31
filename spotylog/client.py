import requests
from .excel_utils import save_to_excel
import requests_cache
from tenacity import retry, stop_after_attempt, wait_exponential

class SpotifyClient:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://api.spotify.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        requests_cache.install_cache("spotify_cache", expire_after=3600)  # Cache expires after 1 hour

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def _get(self, endpoint, params=None):
        """Helper method for GET requests."""
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def _post(self, endpoint, data=None):
        """Helper method for POST requests."""
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def _put(self, endpoint, data=None):
        """Helper method for PUT requests."""
        url = f"{self.base_url}/{endpoint}"
        response = requests.put(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def _delete(self, endpoint, data=None):
        """Helper method for DELETE requests."""
        url = f"{self.base_url}/{endpoint}"
        response = requests.delete(url, headers=self.headers, json=data)
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

    def generate_playlist(self, user_id, name, description="", public=False, tracks=None):
        """
        Generate a playlist with recommended tracks.
        
        Args:
            user_id (str): The user's Spotify ID.
            name (str): The name of the playlist.
            description (str): The playlist description.
            public (bool): Whether the playlist is public.
            tracks (list): A list of track IDs to include.
        """
        if not tracks:
            # Get recommended tracks based on user's top tracks
            top_tracks = self._get("me/top/tracks", params={"limit": 5})
            seed_tracks = ",".join([track["id"] for track in top_tracks["items"]])
            recommendations = self._get("recommendations", params={"seed_tracks": seed_tracks})
            tracks = [track["id"] for track in recommendations["tracks"]]

        # Create the playlist
        playlist = self.create_playlist(user_id, name, description, public)

        # Add tracks to the playlist
        self._post(f"playlists/{playlist['id']}/tracks", data={"uris": [f"spotify:track:{track_id}" for track_id in tracks]})
        return playlist

    def get_recently_played_tracks(self, after=None, before=None, limit=50):
        """
        Fetch recently played tracks within a specific time range.
        
        Args:
            after (int): A Unix timestamp in milliseconds. Fetch tracks played after this time.
            before (int): A Unix timestamp in milliseconds. Fetch tracks played before this time.
            limit (int): The maximum number of tracks to return (default: 50).
        
        Returns:
            list: A list of recently played tracks.
        """
        params = {"limit": limit}
        if after:
            params["after"] = after
        if before:
            params["before"] = before

        response = self._get("me/player/recently-played", params=params)
        return response.get("items", [])

    def get_top_tracks(self, time_range="medium_term", limit=20):
        """
        Fetch the user's top tracks for a specific time range.
        
        Args:
            time_range (str): The time range for the data. Options: "short_term", "medium_term", "long_term".
            limit (int): The maximum number of tracks to return (default: 20).
        
        Returns:
            list: A list of top tracks.
        """
        params = {
            "time_range": time_range,
            "limit": limit,
        }
        response = self._get("me/top/tracks", params=params)
        return response.get("items", [])

    def get_top_artists(self, time_range="medium_term", limit=20):
        """
        Fetch the user's top artists for a specific time range.
        
        Args:
            time_range (str): The time range for the data. Options: "short_term", "medium_term", "long_term".
            limit (int): The maximum number of artists to return (default: 20).
        
        Returns:
            list: A list of top artists.
        """
        params = {
            "time_range": time_range,
            "limit": limit,
        }
        response = self._get("me/top/artists", params=params)
        return response.get("items", [])

    def get_playlist_snapshot(self, playlist_id):
        """
        Fetch a snapshot of a playlist's current state.
        
        Args:
            playlist_id (str): The ID of the playlist.
        
        Returns:
            dict: A snapshot of the playlist's tracks.
        """
        playlist = self._get(f"playlists/{playlist_id}")
        return {
            "id": playlist["id"],
            "name": playlist["name"],
            "tracks": [track["track"]["id"] for track in playlist["tracks"]["items"]],
        }

    def compare_playlist_changes(self, old_snapshot, new_snapshot):
        """
        Compare two playlist snapshots to identify changes.
        
        Args:
            old_snapshot (dict): The old playlist snapshot.
            new_snapshot (dict): The new playlist snapshot.
        
        Returns:
            dict: A dictionary of changes (added_tracks, removed_tracks).
        """
        old_tracks = set(old_snapshot["tracks"])
        new_tracks = set(new_snapshot["tracks"])

        return {
            "added_tracks": list(new_tracks - old_tracks),
            "removed_tracks": list(old_tracks - new_tracks),
        }

    def start_playback(self, device_id=None, context_uri=None, uris=None):
        """
        Start or resume playback on a device.
        
        Args:
            device_id (str): The ID of the device to play on.
            context_uri (str): The context URI (e.g., a playlist or album).
            uris (list): A list of track URIs to play.
        """
        data = {}
        if context_uri:
            data["context_uri"] = context_uri
        if uris:
            data["uris"] = uris
        self._put(f"me/player/play?device_id={device_id}" if device_id else "me/player/play", data=data)

    def pause_playback(self, device_id=None):
        """Pause playback on a device."""
        self._put(f"me/player/pause?device_id={device_id}" if device_id else "me/player/pause")

    def skip_to_next(self, device_id=None):
        """Skip to the next track."""
        self._post(f"me/player/next?device_id={device_id}" if device_id else "me/player/next")

    def skip_to_previous(self, device_id=None):
        """Skip to the previous track."""
        self._post(f"me/player/previous?device_id={device_id}" if device_id else "me/player/previous")

    def set_volume(self, volume_percent, device_id=None):
        """Set the playback volume."""
        self._put(f"me/player/volume?volume_percent={volume_percent}&device_id={device_id}" if device_id else f"me/player/volume?volume_percent={volume_percent}")

    def save_tracks(self, track_ids):
        """Save tracks to the user's library."""
        self._put("me/tracks", data={"ids": track_ids})

    def remove_tracks(self, track_ids):
        """Remove tracks from the user's library."""
        self._delete("me/tracks", data={"ids": track_ids})

    def check_saved_tracks(self, track_ids):
        """Check if tracks are saved in the user's library."""
        response = self._get("me/tracks/contains", params={"ids": ",".join(track_ids)})
        return response

    def get_new_releases(self, limit=20):
        """Fetch new album releases."""
        response = self._get("browse/new-releases", params={"limit": limit})
        return response.get("albums", {}).get("items", [])

    def get_featured_playlists(self, limit=20):
        """Fetch featured playlists."""
        response = self._get("browse/featured-playlists", params={"limit": limit})
        return response.get("playlists", {}).get("items", [])

    def get_recommendations(self, seed_tracks=None, seed_artists=None, seed_genres=None, limit=20):
        """Fetch personalized recommendations."""
        params = {
            "seed_tracks": ",".join(seed_tracks) if seed_tracks else None,
            "seed_artists": ",".join(seed_artists) if seed_artists else None,
            "seed_genres": ",".join(seed_genres) if seed_genres else None,
            "limit": limit,
        }
        response = self._get("recommendations", params=params)
        return response.get("tracks", [])

    def reorder_playlist_tracks(self, playlist_id, range_start, insert_before, range_length=1):
        """Reorder tracks in a playlist."""
        data = {
            "range_start": range_start,
            "insert_before": insert_before,
            "range_length": range_length,
        }
        self._put(f"playlists/{playlist_id}/tracks", data=data)

    def add_tracks_to_playlist(self, playlist_id, track_uris):
        """Add tracks to a playlist."""
        self._post(f"playlists/{playlist_id}/tracks", data={"uris": track_uris})

    def remove_tracks_from_playlist(self, playlist_id, track_uris):
        """Remove tracks from a playlist."""
        self._delete(f"playlists/{playlist_id}/tracks", data={"uris": track_uris})

    def update_playlist_details(self, playlist_id, name=None, description=None, public=None):
        """Update playlist details."""
        data = {}
        if name:
            data["name"] = name
        if description:
            data["description"] = description
        if public is not None:
            data["public"] = public
        self._put(f"playlists/{playlist_id}", data=data)