import os
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8080/callback")

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

    def get_access_token(self):
        """Automate the OAuth2 flow using a local server."""
        auth_url = self.get_authorization_url()
        print(f"Opening browser for authorization: {auth_url}")
        webbrowser.open(auth_url)

        # Start a local server to handle the redirect
        server = self._start_local_server()
        server.handle_request()

        # Parse the authorization response
        query = urlparse(server.authorization_response).query
        params = parse_qs(query)
        code = params.get("code", [None])[0]

        if not code:
            raise Exception("Authorization failed: No code returned.")

        # Fetch the access token
        token = self.oauth.fetch_token(
            TOKEN_URL,
            code=code,
            client_secret=self.client_secret,
        )
        return token

    def _start_local_server(self):
        """Start a local server to handle the OAuth2 redirect."""
        class CallbackHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"Authorization complete. You can close this window.")
                self.server.authorization_response = self.path

        server = HTTPServer(("localhost", 8080), CallbackHandler)
        return server