from pony import orm
from telegram import Update
from telegram.ext import CallbackContext

from bot.bpm_gifs.generator.presets import TEMPLATES
from bot.utils.build_gif_inlines import build_gif_inline
from bot.utils.check_for_song import get_spotify_state
from bot.utils.login_prompt import prompt_login_check
from bot.utils.user_get_from_update import get_user_from_callback_event


@orm.db_session
def handle_gif_selection(update: Update, context: CallbackContext):
    user = get_user_from_callback_event(update)
    if not prompt_login_check(update, user):
        return

    status, song = get_spotify_state(update, user)

    results = []

    for template_key, template in TEMPLATES.items():
        results.append(
            build_gif_inline(
                song=song,
                template=template,
                user=user
            )
        )

    update.inline_query.answer(results, cache_time=0)
