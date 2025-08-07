import os
from dotenv import load_dotenv
from urllib.parse import urlencode
import requests
import base64

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SCOPES = "user-library-read user-read-recently-played"

# Redirect to spotify authorization
def get_spotify_auth_url():
    auth_url = "https://accounts.spotify.com/authorize?"
    params = {
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "scope": SCOPES,
        "show_dialog": "true"
    }
    return auth_url + urlencode(params)

# Use authorization code to receive an access and refresh token
def exchange_code_for_token(code: str):
    url = "https://accounts.spotify.com/api/token"
    auth_str = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI
    }

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()  # Contains access_token, refresh_token, expires_in, etc.