import logging
from typing import Optional

from telegram import Update

from bot.models import User, Song, Spotify


def get_spotify_state(update: Update, user: User) -> tuple[Spotify.Status, Optional[Song]]:
    status = user.spotify.status
    song = status.song
    if not song:
        logging.warning("no song found")

    logging.info("{} - {}".format(song.artist, song.name))

    return status, song