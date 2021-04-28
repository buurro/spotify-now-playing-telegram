import os

from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import Updater

from .models import db

load_dotenv()

if os.getenv("DB_PROVIDER") == "sqlite":
    db.bind(
        provider="sqlite",
        filename=os.getenv("DB_FILENAME"),
        create_db=True,
    )
else:
    db.bind(
        provider=os.getenv("DB_PROVIDER"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_DATABASE"),
    )

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
