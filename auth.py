import os
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

# Spotify API endpoints
AUTHORIZATION_BASE_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"

class SpotifyAuth:
    def __init__(self, client_id=None, client_secret=None, redirect_uri=None):
        self.client_id = client_id or CLIENT_ID
        self.client_secret = client_secret or CLIENT_SECRET
        self.redirect_uri = redirect_uri or REDIRECT_URI
        self.oauth = OAuth2Session(self.client_id, redirect_uri=self.redirect_uri)

    def get_authorization_url(self):
        """Get the URL to authorize the app."""
        authorization_url, _ = self.oauth.authorization_url(AUTHORIZATION_BASE_URL)
        return authorization_url

    def get_access_token(self, authorization_response):
        """Fetch the access token using the authorization response."""
        token = self.oauth.fetch_token(
            TOKEN_URL,
            authorization_response=authorization_response,
            client_secret=self.client_secret,
        )
        return token