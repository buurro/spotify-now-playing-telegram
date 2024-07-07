import os
import typing
from dataclasses import dataclass

from dotenv import load_dotenv
from pony.orm import Database, Optional, Required
from pyfy import ApiError, ClientCreds
from pyfy import Spotify as Pyfy
from pyfy import UserCreds

load_dotenv()

db = Database()


@dataclass
class Image:
    url: str
    height: int
    width: int

    def __init__(self, image: dict):
        self.url = image["url"]
        self.height = int(image["height"] or 0)
        self.width = int(image["width"] or 0)


@dataclass
class SpotifyObject:
    id: str
    name: str
    type: str
    uri: str
    url: str
    thumbnail: Image


@dataclass
class Song(SpotifyObject):
    artist: str

    def __init__(self, song: dict):
        super().__init__(
            id=song["id"],
            url=song["external_urls"]["spotify"],
            uri=song["uri"],
            type=song["type"],
            thumbnail=Image(song["album"]["images"][-1]),
            name=song["name"],
        )
        self.artist = song["artists"][0]["name"]


@dataclass
class Context(SpotifyObject):
    artist: typing.Optional[str]

    def __init__(self, context: dict):
        super().__init__(
            id=context["id"],
            type=context["type"],
            uri=context["uri"],
            url=context["external_urls"]["spotify"],
            thumbnail=Image(context["images"][-1]),
            name=context["name"],
        )
        if "artists" in context:
            self.artist = context["artists"][0]["name"]


class Spotify:
    def __init__(self, user):
        self.user = user

        self._client = SpotifyClient(
            access_token=self.user.spotify_access_token,
            refresh_token=self.user.spotify_refresh_token,
        )

    @dataclass
    class Status:
        song: Song
        context: typing.Any

    @property
    def status(self):
        status = self._client.currently_playing()
        if status:
            song = status["item"]
        else:  # get last played track
            recent_tracks = self._client.recently_played_tracks(limit=1)
            if not recent_tracks:
                return None

            status = recent_tracks["items"][0]
            song = status["track"]
        if not status:
            return None

        song = Song(song)

        context = status["context"]

        # remove the context if sharing from "Liked Songs"
        if context and context["type"] == "collection":
            context = None

        if context:
            context_id = context["uri"].split(":")[-1]
            try:
                context_data = getattr(self._client, context["type"])(context_id)
                context = Context(context_data)
            except ApiError:
                context = None

        return self.Status(song=song, context=context)

    def add_to_queue(self, track_id: str):
        self._client.queue(track_id)


class SpotifyClient(Pyfy):
    def __init__(
        self,
        access_token=None,
        refresh_token=None,
    ):
        scopes = [
            "user-read-recently-played",
            "user-read-playback-state",
            "user-modify-playback-state",
        ]

        user_creds = None

        if access_token and refresh_token:
            user_creds = UserCreds(
                access_token=access_token, refresh_token=refresh_token
            )

        super().__init__(
            client_creds=ClientCreds(
                client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
                redirect_uri=os.getenv("SPOTIFY_CLIENT_REDIRECT"),
                scopes=scopes,
            ),
            user_creds=user_creds,
        )

    def artist(self, *args, **kwargs):
        return super().artists(*args, **kwargs)

    def album(self, *args, **kwargs):
        return super().albums(*args, **kwargs)


class User(db.Entity):
    telegram_id = Required(str)
    # FIXME it generates NOT NULL constraint failed: user.spotify_id
    spotify_id = Optional(str)
    spotify_access_token = Optional(str)
    spotify_refresh_token = Optional(str)
    # modify_playback_state = Required(bool, default=False)
    # allowed_scopes = Required(List(str))

    @property
    def spotify(self) -> Spotify:
        return Spotify(self)
