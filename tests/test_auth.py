import sys
import os

# Add the root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import patch
from spotylog.auth import SpotifyAuth

# Test get_authorization_url functionality
def test_get_authorization_url():
    auth = SpotifyAuth()
    auth_url = auth.get_authorization_url()

    # Assert the URL is generated correctly
    assert "https://accounts.spotify.com/authorize" in auth_url

# Test get_access_token functionality
def test_get_access_token():
    with patch("spotylog.auth.HTTPServer") as mock_server, patch("webbrowser.open") as mock_browser:
        # Mock the server and browser
        mock_server_instance = mock_server.return_value
        mock_server_instance.authorization_response = "/callback?code=dummy_code"

        # Mock the OAuth2Session
        with patch("spotylog.auth.OAuth2Session.fetch_token") as mock_fetch_token:
            mock_fetch_token.return_value = {"access_token": "dummy_token"}

            # Call the get_access_token method
            auth = SpotifyAuth()
            token = auth.get_access_token()

            # Assert the token is returned
            assert token == {"access_token": "dummy_token"}