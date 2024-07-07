from uuid import uuid4

from telegram import InlineQueryResultMpeg4Gif, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton

from bot.bpm_gifs.generator.presets import GifTemplate
from bot.models import Song, User
from bot.utils.format_song import format_song_markdown


def build_gif_inline(song: Song, template: GifTemplate, user: User):
    song_bpm = user.spotify.get_song_bpm(song)

    return InlineQueryResultMpeg4Gif(
        id=str(uuid4()),
        title=f"{int(song_bpm)} BPM: {song.artist} - {song.name}",
        url=song.url,

        mpeg4_url=template.build_bpm_url(target_bpm=song_bpm),
        mpg4_width=template.wh[0],
        mpg4_height=template.wh[1],

        thumb_url=template.build_preview_url(),
        thumb_width=template.wh[0],
        thumb_height=template.wh[1],

        caption=f"{int(song_bpm)} BPM: {format_song_markdown(song)}",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Open on Spotify", url=song.url),
                    InlineKeyboardButton(text="Add to queue", callback_data="queue;" + song.id),
                ]
            ]
        ),
    )
