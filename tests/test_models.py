import sys
import os

# Add the root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from spotylog.models import Track, Playlist

# Test Track class
def test_track():
    track_data = {
        "id": "track_id",
        "name": "Believer",
        "artists": [{"name": "Imagine Dragons"}],
        "album": {"name": "Evolve"}
    }
    track = Track(track_data)

    # Assert the track attributes
    assert track.name == "Believer"
    assert track.artists == ["Imagine Dragons"]
    assert track.album == "Evolve"
    assert str(track) == "Believer by Imagine Dragons"

# Test Playlist class
def test_playlist():
    playlist_data = {
        "id": "playlist_id",
        "name": "My Playlist",
        "description": "A test playlist",
        "tracks": {
            "items": [
                {"track": {"id": "track_id_1"}},
                {"track": {"id": "track_id_2"}}
            ]
        }
    }
    playlist = Playlist(playlist_data)

    # Assert the playlist attributes
    assert playlist.name == "My Playlist"
    assert playlist.description == "A test playlist"
    assert len(playlist.tracks) == 2
    assert str(playlist) == "My Playlist - 2 tracks"