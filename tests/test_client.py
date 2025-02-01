import sys
import os

# Add the root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import Mock, patch
from spotylog.client import SpotifyClient

# Fixture to create a mock SpotifyClient instance
@pytest.fixture
def mock_client():
    # Mock the access token
    client = SpotifyClient("dummy_access_token")
    return client

# Test search functionality
def test_search(mock_client):
    with patch("requests.get") as mock_get:
        # Mock the API response
        mock_get.return_value.json.return_value = {
            "tracks": {
                "items": [
                    {"name": "Believer", "artists": [{"name": "Imagine Dragons"}], "album": {"name": "Evolve"}}
                ]
            }
        }
        mock_get.return_value.raise_for_status.return_value = None

        # Call the search method
        results = mock_client.search("Imagine Dragons")

        # Assert the results
        assert "tracks" in results
        assert results["tracks"]["items"][0]["name"] == "Believer"

# Test get_user_playlists functionality
def test_get_user_playlists(mock_client):
    with patch("requests.get") as mock_get:
        # Mock the API response
        mock_get.return_value.json.return_value = {
            "items": [
                {"name": "My Playlist", "description": "A test playlist", "owner": {"display_name": "User"}, "tracks": {"total": 10}, "public": True}
            ]
        }
        mock_get.return_value.raise_for_status.return_value = None

        # Call the get_user_playlists method
        playlists = mock_client.get_user_playlists()

        # Assert the results
        assert "items" in playlists
        assert playlists["items"][0]["name"] == "My Playlist"

# Test create_playlist functionality
def test_create_playlist(mock_client):
    with patch("requests.post") as mock_post:
        # Mock the API response
        mock_post.return_value.json.return_value = {
            "id": "playlist_id",
            "name": "New Playlist",
            "description": "A new playlist",
            "public": False
        }
        mock_post.return_value.raise_for_status.return_value = None

        # Call the create_playlist method
        playlist = mock_client.create_playlist("user_id", "New Playlist", "A new playlist", False)

        # Assert the results
        assert playlist["name"] == "New Playlist"
        assert playlist["description"] == "A new playlist"

# Test save_search_results_to_excel functionality
def test_save_search_results_to_excel(mock_client):
    with patch("requests.get") as mock_get:
        # Mock the API response
        mock_get.return_value.json.return_value = {
            "tracks": {
                "items": [
                    {"name": "Believer", "artists": [{"name": "Imagine Dragons"}], "album": {"name": "Evolve"}, "duration_ms": 204000, "popularity": 85}
                ]
            }
        }
        mock_get.return_value.raise_for_status.return_value = None

        # Call the save_search_results_to_excel method
        mock_client.save_search_results_to_excel("Imagine Dragons", filename="test_search_results.xlsx")

        # Assert the file was created
        assert os.path.exists("test_search_results.xlsx")
        os.remove("test_search_results.xlsx")  # Clean up

# Test save_user_playlists_to_excel functionality
def test_save_user_playlists_to_excel(mock_client):
    with patch("requests.get") as mock_get:
        # Mock the API response
        mock_get.return_value.json.return_value = {
            "items": [
                {"name": "My Playlist", "description": "A test playlist", "owner": {"display_name": "User"}, "tracks": {"total": 10}, "public": True}
            ]
        }
        mock_get.return_value.raise_for_status.return_value = None

        # Call the save_user_playlists_to_excel method
        mock_client.save_user_playlists_to_excel(filename="test_user_playlists.xlsx")

        # Assert the file was created
        assert os.path.exists("test_user_playlists.xlsx")
        os.remove("test_user_playlists.xlsx")  # Clean up

# Test get_recently_played_tracks functionality
def test_get_recently_played_tracks(mock_client):
    with patch("requests.get") as mock_get:
        # Mock the API response
        mock_get.return_value.json.return_value = {
            "items": [
                {"track": {"name": "Believer", "artists": [{"name": "Imagine Dragons"}], "album": {"name": "Evolve"}}, "played_at": "2023-10-01T12:00:00Z"}
            ]
        }
        mock_get.return_value.raise_for_status.return_value = None

        # Call the get_recently_played_tracks method
        tracks = mock_client.get_recently_played_tracks()

        # Assert the results
        assert "items" in tracks
        assert tracks["items"][0]["track"]["name"] == "Believer"

# Test get_top_tracks functionality
def test_get_top_tracks(mock_client):
    with patch("requests.get") as mock_get:
        # Mock the API response
        mock_get.return_value.json.return_value = {
            "items": [
                {"name": "Believer", "artists": [{"name": "Imagine Dragons"}], "album": {"name": "Evolve"}}
            ]
        }
        mock_get.return_value.raise_for_status.return_value = None

        # Call the get_top_tracks method
        tracks = mock_client.get_top_tracks()

        # Assert the results
        assert "items" in tracks
        assert tracks["items"][0]["name"] == "Believer"

# Test get_top_artists functionality
def test_get_top_artists(mock_client):
    with patch("requests.get") as mock_get:
        # Mock the API response
        mock_get.return_value.json.return_value = {
            "items": [
                {"name": "Imagine Dragons", "genres": ["rock"], "popularity": 85}
            ]
        }
        mock_get.return_value.raise_for_status.return_value = None

        # Call the get_top_artists method
        artists = mock_client.get_top_artists()

        # Assert the results
        assert "items" in artists
        assert artists["items"][0]["name"] == "Imagine Dragons"

# Test get_playlist_snapshot functionality
def test_get_playlist_snapshot(mock_client):
    with patch("requests.get") as mock_get:
        # Mock the API response
        mock_get.return_value.json.return_value = {
            "id": "playlist_id",
            "name": "My Playlist",
            "tracks": {
                "items": [
                    {"track": {"id": "track_id_1"}},
                    {"track": {"id": "track_id_2"}}
                ]
            }
        }
        mock_get.return_value.raise_for_status.return_value = None

        # Call the get_playlist_snapshot method
        snapshot = mock_client.get_playlist_snapshot("playlist_id")

        # Assert the results
        assert snapshot["id"] == "playlist_id"
        assert len(snapshot["tracks"]) == 2

# Test compare_playlist_changes functionality
def test_compare_playlist_changes(mock_client):
    old_snapshot = {
        "id": "playlist_id",
        "name": "My Playlist",
        "tracks": ["track_id_1", "track_id_2"]
    }
    new_snapshot = {
        "id": "playlist_id",
        "name": "My Playlist",
        "tracks": ["track_id_2", "track_id_3"]
    }

    # Call the compare_playlist_changes method
    changes = mock_client.compare_playlist_changes(old_snapshot, new_snapshot)

    # Assert the results
    assert changes["added_tracks"] == ["track_id_3"]
    assert changes["removed_tracks"] == ["track_id_1"]

# Test start_playback functionality
def test_start_playback(mock_client):
    with patch("requests.put") as mock_put:
        # Mock the API response
        mock_put.return_value.raise_for_status.return_value = None

        # Call the start_playback method
        mock_client.start_playback(device_id="device_id")

        # Assert the request was made
        mock_put.assert_called_once()

# Test pause_playback functionality
def test_pause_playback(mock_client):
    with patch("requests.put") as mock_put:
        # Mock the API response
        mock_put.return_value.raise_for_status.return_value = None

        # Call the pause_playback method
        mock_client.pause_playback(device_id="device_id")

        # Assert the request was made
        mock_put.assert_called_once()

# Test skip_to_next functionality
def test_skip_to_next(mock_client):
    with patch("requests.post") as mock_post:
        # Mock the API response
        mock_post.return_value.raise_for_status.return_value = None

        # Call the skip_to_next method
        mock_client.skip_to_next(device_id="device_id")

        # Assert the request was made
        mock_post.assert_called_once()

# Test skip_to_previous functionality
def test_skip_to_previous(mock_client):
    with patch("requests.post") as mock_post:
        # Mock the API response
        mock_post.return_value.raise_for_status.return_value = None

        # Call the skip_to_previous method
        mock_client.skip_to_previous(device_id="device_id")

        # Assert the request was made
        mock_post.assert_called_once()

# Test set_volume functionality
def test_set_volume(mock_client):
    with patch("requests.put") as mock_put:
        # Mock the API response
        mock_put.return_value.raise_for_status.return_value = None

        # Call the set_volume method
        mock_client.set_volume(volume_percent=50, device_id="device_id")

        # Assert the request was made
        mock_put.assert_called_once()

# Test save_tracks functionality
def test_save_tracks(mock_client):
    with patch("requests.put") as mock_put:
        # Mock the API response
        mock_put.return_value.raise_for_status.return_value = None

        # Call the save_tracks method
        mock_client.save_tracks(["track_id_1", "track_id_2"])

        # Assert the request was made
        mock_put.assert_called_once()

# Test remove_tracks functionality
def test_remove_tracks(mock_client):
    with patch("requests.delete") as mock_delete:
        # Mock the API response
        mock_delete.return_value.raise_for_status.return_value = None

        # Call the remove_tracks method
        mock_client.remove_tracks(["track_id_1", "track_id_2"])

        # Assert the request was made
        mock_delete.assert_called_once()

# Test check_saved_tracks functionality
def test_check_saved_tracks(mock_client):
    with patch("requests.get") as mock_get:
        # Mock the API response
        mock_get.return_value.json.return_value = [True, False]
        mock_get.return_value.raise_for_status.return_value = None

        # Call the check_saved_tracks method
        results = mock_client.check_saved_tracks(["track_id_1", "track_id_2"])

        # Assert the results
        assert results == [True, False]

# Test get_new_releases functionality
def test_get_new_releases(mock_client):
    with patch("requests.get") as mock_get:
        # Mock the API response
        mock_get.return_value.json.return_value = {
            "albums": {
                "items": [
                    {"name": "New Album", "artists": [{"name": "Artist"}], "release_date": "2023-10-01", "total_tracks": 10}
                ]
            }
        }
        mock_get.return_value.raise_for_status.return_value = None

        # Call the get_new_releases method
        new_releases = mock_client.get_new_releases()

        # Assert the results
        assert "albums" in new_releases
        assert new_releases["albums"]["items"][0]["name"] == "New Album"

# Test get_featured_playlists functionality
def test_get_featured_playlists(mock_client):
    with patch("requests.get") as mock_get:
        # Mock the API response
        mock_get.return_value.json.return_value = {
            "playlists": {
                "items": [
                    {"name": "Featured Playlist", "description": "A featured playlist", "owner": {"display_name": "Spotify"}, "tracks": {"total": 20}, "public": True}
                ]
            }
        }
        mock_get.return_value.raise_for_status.return_value = None

        # Call the get_featured_playlists method
        playlists = mock_client.get_featured_playlists()

        # Assert the results
        assert "playlists" in playlists
        assert playlists["playlists"]["items"][0]["name"] == "Featured Playlist"

# Test get_recommendations functionality
def test_get_recommendations(mock_client):
    with patch("requests.get") as mock_get:
        # Mock the API response
        mock_get.return_value.json.return_value = {
            "tracks": [
                {"name": "Recommended Track", "artists": [{"name": "Artist"}], "album": {"name": "Album"}}
            ]
        }
        mock_get.return_value.raise_for_status.return_value = None

        # Call the get_recommendations method
        recommendations = mock_client.get_recommendations(seed_tracks=["track_id_1"])

        # Assert the results
        assert "tracks" in recommendations
        assert recommendations["tracks"][0]["name"] == "Recommended Track"

# Test reorder_playlist_tracks functionality
def test_reorder_playlist_tracks(mock_client):
    with patch("requests.put") as mock_put:
        # Mock the API response
        mock_put.return_value.raise_for_status.return_value = None

        # Call the reorder_playlist_tracks method
        mock_client.reorder_playlist_tracks("playlist_id", range_start=0, insert_before=1)

        # Assert the request was made
        mock_put.assert_called_once()

# Test add_tracks_to_playlist functionality
def test_add_tracks_to_playlist(mock_client):
    with patch("requests.post") as mock_post:
        # Mock the API response
        mock_post.return_value.raise_for_status.return_value = None

        # Call the add_tracks_to_playlist method
        mock_client.add_tracks_to_playlist("playlist_id", ["track_id_1", "track_id_2"])

        # Assert the request was made
        mock_post.assert_called_once()

# Test remove_tracks_from_playlist functionality
def test_remove_tracks_from_playlist(mock_client):
    with patch("requests.delete") as mock_delete:
        # Mock the API response
        mock_delete.return_value.raise_for_status.return_value = None

        # Call the remove_tracks_from_playlist method
        mock_client.remove_tracks_from_playlist("playlist_id", ["track_id_1", "track_id_2"])

        # Assert the request was made
        mock_delete.assert_called_once()

# Test update_playlist_details functionality
def test_update_playlist_details(mock_client):
    with patch("requests.put") as mock_put:
        # Mock the API response
        mock_put.return_value.raise_for_status.return_value = None

        # Call the update_playlist_details method
        mock_client.update_playlist_details("playlist_id", name="Updated Playlist", description="Updated Description", public=True)

        # Assert the request was made
        mock_put.assert_called_once()