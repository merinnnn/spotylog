import pytest
from spotylog import SpotifyClient

@pytest.fixture
def client():
    return SpotifyClient("dummy_access_token")

def test_search(client):
    results = client.search("Imagine Dragons")
    assert "tracks" in results

def test_get_user_playlists(client):
    playlists = client.get_user_playlists()
    assert "items" in playlists