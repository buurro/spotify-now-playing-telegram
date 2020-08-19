from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import Updater
from models import db

import os


load_dotenv()

db.bind(provider="sqlite", filename="database.sqlite", create_db=True)
db.generate_mapping(create_tables=True)

bot = Bot(os.getenv("TELEGRAM_TOKEN"))

# Create the Updater and pass it your bot's token.
# Make sure to set use_context=True to use the new context based callbacks
# Post version 12 this will no longer be necessary
updater = Updater(os.getenv("TELEGRAM_TOKEN"), use_context=True)

bot_description = """
This bot works in all your chats and groups, there's no need to add it anywhere.

Simply type in any chat @spnpbot, then a whitespace.

This will open a panel with a preview of the song you are currently playing on Spotify. Tap on it to send the song right away.
"""

animation_id = os.getenv("TELEGRAM_ANIMATION_ID")

app_port = os.getenv("TORNADO_PORT")
