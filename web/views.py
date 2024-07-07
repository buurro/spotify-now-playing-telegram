import logging

import tornado.web
from pony import orm
from telegram import ReplyKeyboardRemove

from bot.bpm_gifs.generator.presets import TEMPLATES
from bot.models import SpotifyClient, User
from bot.utils.config import animation_id, bot, bot_description


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class GifPreviewHandler(tornado.web.RequestHandler):
    def get(self):
        template_name = self.get_argument("t", None)
        preset = TEMPLATES.get(template_name)
        self.set_header("Content-Type", "image/png")
        preview_content = preset.get_preview_content()
        self.write(preview_content)


class GifRenderHandler(tornado.web.RequestHandler):
    def get(self):
        template_name = self.get_argument("t", None)
        target_bpm = self.get_argument("bpm", "60.0")
        target_bpm = float(target_bpm)

        if target_bpm < 20:
            raise ValueError("Target BPM must be greater than 20")
        if target_bpm > 300:
            raise ValueError("Target BPM must be less than 200")

        preset = TEMPLATES.get(template_name)

        self.set_header("Content-Type", "video/mp4")
        preview_content = preset.render_as_target_bpm(target_bpm)
        self.write(preview_content)


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
                    user.spotify_id = user_creds.id or "FIXME"
                    #FIXME: spotify user id is not using atm but
                    # migration issue probably
                    user.spotify_access_token = user_creds.access_token
                    user.spotify_refresh_token = user_creds.refresh_token
                else:
                    user = User(
                        telegram_id=callback_state,
                        spotify_id=user_creds.id or "FIXME",
                        #FIXME: spotify user id is not using atm but migration
                        # issue probably
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


urls = [
    (r"/", MainHandler),
    (r"/spotify/callback", SpotifyCallback),
    (r"/gif/preview", GifPreviewHandler),
    (r"/gif/bpm", GifRenderHandler),
]
