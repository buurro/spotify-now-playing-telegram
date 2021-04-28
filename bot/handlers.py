from telegram.ext import CallbackQueryHandler, CommandHandler, InlineQueryHandler

from .callbacks import callback_query, help, inlinequery, start

handlers = [
    CommandHandler("start", start),
    CommandHandler("help", help),
    InlineQueryHandler(inlinequery),
    CallbackQueryHandler(callback_query),
]
