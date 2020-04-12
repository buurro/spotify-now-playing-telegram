from pyfy import Spotify, ClientCreds, UserCreds
from utils import config

# Init pyfy
spotify = Spotify()
client_creds = ClientCreds(
    client_id=config["spotify"]["client_id"],
    client_secret=config["spotify"]["client_secret"],
    redirect_uri=config["spotify"]["client_redirect"],
    scopes=["user-read-recently-played", "user-read-playback-state"],
)
spotify.client_creds = client_creds


def get_credentials(user):
    return UserCreds(
        access_token=user.spotify_access_token, refresh_token=user.spotify_refresh_token
    )
