from telegram.ext import CallbackQueryHandler, CommandHandler, InlineQueryHandler
from .bpm_gifs.gif_handler import handle_gif_selection

from .callbacks import callback_query, help, inline_share_song, start

handlers = [
    CommandHandler("start", start),
    CommandHandler("help", help),
    InlineQueryHandler(handle_gif_selection, pattern=r"gif"),
    InlineQueryHandler(inline_share_song),
    CallbackQueryHandler(callback_query),
]
