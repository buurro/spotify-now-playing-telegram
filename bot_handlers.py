from telegram.ext import CommandHandler, InlineQueryHandler
from bot_callbacks import start, help, inlinequery

command_handlers = [
    CommandHandler("start", start),
    CommandHandler("help", help),
    InlineQueryHandler(inlinequery),
]
