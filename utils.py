from configparser import ConfigParser

from telegram import Bot
from telegram.ext import Updater

from models import db

# Load config.ini
config = ConfigParser()
config.read("config.ini")

db.bind(provider="sqlite", filename="database.sqlite", create_db=True)
db.generate_mapping(create_tables=True)

bot = Bot(config["telegram"]["token"])

# Create the Updater and pass it your bot's token.
# Make sure to set use_context=True to use the new context based callbacks
# Post version 12 this will no longer be necessary
updater = Updater(config["telegram"]["token"], use_context=True)
