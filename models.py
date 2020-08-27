from pony.orm import Database, Required, Optional
from pyfy import Spotify as Pyfy, ClientCreds, UserCreds
from pyfy.excs import ApiError
from dotenv import load_dotenv
from dataclasses import dataclass

import typing
import os


load_dotenv()

db = Database()


@dataclass
class SpotifyObject:
    id: str
    type: str
    uri: str
    url: str


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
class Song(SpotifyObject):
    artist: str
    thumbnail: Image
    name: str

    def __init__(self, song: dict):
        super().__init__(
            id=song["id"],
            url=song["external_urls"]["spotify"],
            uri=song["uri"],
            type=song["type"]
        )
        self.name = song["name"]
        self.artist = song["artists"][0]["name"]
        self.thumbnail = Image(song["album"]["images"][-1])


@dataclass
class Album(SpotifyObject):
    artist: str
    thumbnail: Image
    name: str

    def __init__(self, album: dict):
        super().__init__(
            id=album["id"],
            url=album["external_urls"]["spotify"],
            uri=album["uri"],
            type=album["type"]
        )
        self.name = album["name"]
        self.artist = album["artists"][0]["name"]
        self.thumbnail = Image(album["images"][-1])


@dataclass
class Playlist(SpotifyObject):
    name: str
    thumbnail: Image


    def __init__(self, playlist: dict):
        super().__init__(
            id=playlist["id"],
            url=playlist["external_urls"]["spotify"],
            uri=playlist["uri"],
            type=playlist["type"]
        )
        self.name = playlist["name"]
        self.thumbnail = Image(playlist["images"][-1])


@dataclass
class Context(SpotifyObject):
    playlist: Playlist

    def __init__(self, context: dict):
        context_id = context["uri"].split(":")[-1]
        super().__init__(
            id=context_id,
            type=context["type"],
            uri=context["uri"],
            url=context["href"]
        )



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
            song = Song(status["item"])
            context = Context(status["context"])
            if context.type == "playlist":
                context = self._client.playlist(context.id)
            elif context.type == "album":
                context = self._client.album(context.id)

            return self.Status(song=song, context=context)


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
                client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
                redirect_uri=os.getenv("SPOTIFY_CLIENT_REDIRECT"),
                scopes=scopes,
            ),
            user_creds=user_creds,
        )

    def playlist(self, id):
        return Playlist(super().playlist(id))

    def album(self, id):
        return Album(super().albums(id))


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
