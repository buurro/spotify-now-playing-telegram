import logging

import tornado.web
from bot.models import SpotifyClient, User
from bot.utils import animation_id, bot, bot_description
from pony import orm
from telegram import ReplyKeyboardRemove


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class SpotifyCallback(tornado.web.RequestHandler):
    @orm.db_session
    def get(self):
        if self.get_argument("code", ""):
            grant = self.get_argument("code", "")
            callback_state = self.get_argument("state", "")
            if not callback_state:
                self.write("spotify no callback state")
            spotify = SpotifyClient()
            try:
                user_creds = spotify.build_user_creds(grant=grant)
            except:
                self.write("spotify build user creds error")
            else:
                user = User.get(telegram_id=callback_state)
                if user:
                    user.spotify_id = user_creds.id
                    user.spotify_access_token = user_creds.access_token
                    user.spotify_refresh_token = user_creds.refresh_token
                else:
                    user = User(
                        telegram_id=callback_state,
                        spotify_id=user_creds.id,
                        spotify_access_token=user_creds.access_token,
                        spotify_refresh_token=user_creds.refresh_token,
                    )

                orm.commit()
                logging.info("User logged in")
                bot.sendMessage(
                    callback_state,
                    "Successfully logged in!",
                    reply_markup=ReplyKeyboardRemove(),
                )
                if animation_id:
                    bot.sendAnimation(callback_state, animation_id)
                bot.sendMessage(callback_state, bot_description)
                self.redirect("https://t.me/" + bot.username)

        else:
            self.write("spotify no code")


urls = [(r"/", MainHandler), (r"/spotify/callback", SpotifyCallback)]
