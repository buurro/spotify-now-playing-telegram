from telegram.ext import CallbackQueryHandler, CommandHandler, InlineQueryHandler

from .callbacks import callback_query, help, inline_share_song, start

handlers = [
    CommandHandler("start", start),
    CommandHandler("help", help),
    InlineQueryHandler(inline_share_song),
    CallbackQueryHandler(callback_query),
]
