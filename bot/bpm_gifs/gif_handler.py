from uuid import uuid4

from pony import orm
from telegram import InlineKeyboardButton as Button, InlineQueryResultMpeg4Gif
from telegram import (
    InlineKeyboardMarkup,
    ParseMode,
)
from telegram import Update
from telegram.ext import CallbackContext

from bot.bpm_gifs.generator.presets import TEMPLATES
from bot.utils.check_for_song import get_spotify_state
from bot.utils.format_song import format_song_markdown
from bot.utils.login_prompt import prompt_login_check
from bot.utils.user_get_from_update import get_user_from_callback_event


@orm.db_session
def handle_gif_selection(update: Update, context: CallbackContext):
    """Handle the inline query."""
    user = get_user_from_callback_event(update)
    if not prompt_login_check(update, user):
        return

    status, song = get_spotify_state(update, user)
    bpm = user.spotify.get_song_bpm(song)

    results = []

    song_bpm = user.spotify.get_song_bpm(song)

    for template_key, template in TEMPLATES.items():
        results.append(
            InlineQueryResultMpeg4Gif(
                id=uuid4(),
                title=f"{int(bpm)} BPM: {song.artist} - {song.name}",
                url=song.url,

                mpeg4_url=template.build_bpm_url(target_bpm=song_bpm),
                mpg4_width=template.wh[0],
                mpg4_height=template.wh[1],

                thumb_url=template.build_preview_url(),
                thumb_width=template.wh[0],
                thumb_height=template.wh[1],

                caption=f"{int(bpm)} BPM: {format_song_markdown(song)}",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            Button(text="Open on Spotify", url=song.url),
                            Button(text="Add to queue", callback_data="queue;" + song.id),
                        ]
                    ]
                ),
            )
        )
    update.inline_query.answer(results, cache_time=0)
