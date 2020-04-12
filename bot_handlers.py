from telegram.ext import CommandHandler, InlineQueryHandler, CallbackQueryHandler
from bot_callbacks import start, help, inlinequery, callback_query

"""
login_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        0: [
            MessageHandler(Filters.regex("^(Yes|yes|y)$"), login_with_permissions),
            MessageHandler(Filters.regex("^(No|no|n)$"), login_without_permissions),
        ]
    },
    fallbacks=[MessageHandler(Filters.text, login_fallback)]
)
"""

handlers = [
    CommandHandler("start", start),
    CommandHandler("help", help),
    InlineQueryHandler(inlinequery),
    CallbackQueryHandler(callback_query),
]
