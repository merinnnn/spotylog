import sys
import os

# Add the root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import patch
from spotylog.cli import main

# Test CLI search functionality
def test_cli_search():
    with patch("spotylog.cli.SpotifyAuth") as mock_auth, patch("spotylog.cli.SpotifyClient") as mock_client:
        # Mock the authentication and client
        mock_auth.return_value.get_access_token.return_value = {"access_token": "dummy_token"}
        mock_client.return_value.search.return_value = {
            "tracks": {
                "items": [
                    {"name": "Believer", "artists": [{"name": "Imagine Dragons"}], "album": {"name": "Evolve"}}
                ]
            }
        }

        # Simulate CLI arguments
        with patch("sys.argv", ["cli.py", "--search", "Imagine Dragons"]):
            main()

        # Assert the search method was called
        mock_client.return_value.search.assert_called_once_with("Imagine Dragons")

# Test CLI export functionality
def test_cli_export():
    with patch("spotylog.cli.SpotifyAuth") as mock_auth, patch("spotylog.cli.SpotifyClient") as mock_client:
        # Mock the authentication and client
        mock_auth.return_value.get_access_token.return_value = {"access_token": "dummy_token"}
        mock_client.return_value.search.return_value = {
            "tracks": {
                "items": [
                    {"name": "Believer", "artists": [{"name": "Imagine Dragons"}], "album": {"name": "Evolve"}}
                ]
            }
        }

        # Simulate CLI arguments
        with patch("sys.argv", ["cli.py", "--search", "Imagine Dragons", "--export", "excel"]):
            main()

        # Assert the save_search_results_to_excel method was called
        mock_client.return_value.save_search_results_to_excel.assert_called_once_with("Imagine Dragons", filename="search_results.xlsx")