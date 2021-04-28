import os

from dotenv import load_dotenv
from pyfy import ClientCreds, Spotify, UserCreds

load_dotenv()

# Init pyfy
spotify = Spotify()
client_creds = ClientCreds(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_CLIENT_REDIRECT"),
    scopes=["user-read-recently-played", "user-read-playback-state"],
)
spotify.client_creds = client_creds


def get_credentials(user):
    return UserCreds(
        access_token=user.spotify_access_token, refresh_token=user.spotify_refresh_token
    )
