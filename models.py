from pony.orm import Database, Required, Optional
from pyfy import Spotify as Pyfy, ClientCreds, UserCreds
from pyfy.excs import ApiError
from configparser import ConfigParser
from dataclasses import dataclass

import typing


config = ConfigParser()
config.read("config.ini")

db = Database()


@dataclass
class Image:
    url: str
    height: int
    width: int

    def __init__(self, image: dict):
        self.url = image["url"]
        self.height = image["height"]
        self.width = image["width"]


@dataclass
class Song:
    id: str
    name: str
    artist: str
    url: str
    thumbnail: Image

    def __init__(self, song: dict):
        self.id = song["id"]
        self.name = song["name"]
        self.artist = song["artists"][0]["name"]
        self.url = song["external_urls"]["spotify"]
        self.thumbnail = Image(song["album"]["images"][-1])


class Spotify:
    def __init__(self, user):
        self.user = user

        self._client = SpotifyClient(
            access_token=self.user.spotify_access_token,
            refresh_token=self.user.spotify_refresh_token,
        )

    @property
    def current_song(self) -> typing.Optional[Song]:
        current_status = self._client.currently_playing()
        if current_status:
            song = current_status["item"]
            return Song(song)

    @property
    def last_song(self) -> Song:
        song = self._client.recently_played_tracks(limit=1)["items"][0]["track"]
        return Song(song)

    def add_to_queue(self, track_id: str):
        self._client.queue(track_id)


class SpotifyClient(Pyfy):
    def __init__(
        self,
        access_token=None,
        refresh_token=None,
        # modify_playback_state=False
    ):
        scopes = [
            "user-read-recently-played",
            "user-read-playback-state",
            "user-modify-playback-state",
        ]

        """
        if modify_playback_state:
            scopes.append("user-modify-playback-state")
        """

        user_creds = None

        if access_token and refresh_token:
            user_creds = UserCreds(
                access_token=access_token, refresh_token=refresh_token
            )

        super().__init__(
            client_creds=ClientCreds(
                client_id=config["spotify"]["client_id"],
                client_secret=config["spotify"]["client_secret"],
                redirect_uri=config["spotify"]["client_redirect"],
                scopes=scopes,
            ),
            user_creds=user_creds,
        )


class User(db.Entity):
    telegram_id = Required(str)
    spotify_id = Optional(str)
    spotify_access_token = Optional(str)
    spotify_refresh_token = Optional(str)
    # modify_playback_state = Required(bool, default=False)
    # allowed_scopes = Required(List(str))

    @property
    def spotify(self):
        return Spotify(self)
