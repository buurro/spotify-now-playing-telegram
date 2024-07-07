from telegram import Update

from bot.models import User

def prompt_login_check(update: Update, user: User) -> bool:
    if not user or not user.spotify:
        update.inline_query.answer(
            [],
            switch_pm_text="Login with Spotify",
            switch_pm_parameter="spotify_log_in",
            cache_time=0,
        )
        return False
    return True