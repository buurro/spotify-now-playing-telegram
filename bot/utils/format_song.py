from telegram.utils.helpers import escape_markdown

from bot.models import Song


def format_song_markdown(song: Song):
    return "🎵 `{author} - {song_name}`\n [Spotify]({song_spoti_link}) | [Other]({other_link})".format(
        song_name=song.name,
        song_spoti_link=song.url,
        author=song.artist,
        other_link=escape_markdown(f"https://song.link/s/{song.id}")
    )
