from telegram import Update

from bot.models import User


def get_user_from_callback_event(update: Update) -> User:
    user_id = str(update.inline_query.from_user.id)
    user: User = User.get(telegram_id=user_id)
    return user
