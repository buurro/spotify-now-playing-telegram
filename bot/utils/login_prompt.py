from telegram import Update

from bot.models import User


def prompt_login_check(update: Update, user: User) -> bool:
    if user and user.spotify:
        return True

    update.inline_query.answer(
        [],
        switch_pm_text="Login with Spotify",
        switch_pm_parameter="spotify_log_in",
        cache_time=0,
    )
    return False
