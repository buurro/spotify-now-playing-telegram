from uuid import uuid4
from pony import orm
from telegram import (
    ParseMode,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineKeyboardButton as Button,
    ReplyKeyboardMarkup,
)
from telegram.utils.helpers import escape_markdown
from datetime import datetime
from pyfy.excs import AuthError, ApiError
from models import User, SpotifyClient
from utils import bot_description


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(bot_description)


@orm.db_session
def get_login_message(user_id):
    spotify = SpotifyClient()
    if spotify.is_oauth_ready:
        url = spotify.auth_uri(state=user_id)
        reply_text = "Tap the button below to log in with your Spotify account"
        reply_markup = InlineKeyboardMarkup(
            inline_keyboard=[[Button(text="Login", url=url)]]
        )
        return reply_text, reply_markup
    else:
        reply_text = "There's something wrong"
        return reply_text, None


def start(update, context):
    user_id = str(update.message.from_user.id)
    reply_text, reply_markup = get_login_message(user_id)
    update.message.reply_text(reply_text, reply_markup=reply_markup)


def login_fallback(update, context):
    keyboard = ReplyKeyboardMarkup([["Yes", "No"]], one_time_keyboard=True)

    update.message.reply_text("Please answer Yes or No", reply_markup=keyboard)

    return 0


@orm.db_session
def inlinequery(update, context):
    """Handle the inline query."""
    user_id = str(update.inline_query.from_user.id)
    user = User.get(telegram_id=user_id)
    if not user or not user.spotify:
        update.inline_query.answer(
            [],
            switch_pm_text="Login with Spotify",
            switch_pm_parameter="spotify_log_in",
            cache_time=0,
        )
        return

    status = user.spotify.status
    song = status.song
    if not song:
        song = user.spotify.last_song

    print("{} | {} - {}".format(datetime.now(), song.artist, song.name))

    thumb = song.thumbnail
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="{} - {}".format(song.artist, song.name),
            url=song.url,
            thumb_url=thumb.url,
            thumb_width=thumb.width,
            thumb_height=thumb.height,
            input_message_content=InputTextMessageContent(
                "🎵 [{}]({}) by {}".format(
                    escape_markdown(song.name), song.url, escape_markdown(song.artist)
                ),
                parse_mode=ParseMode.MARKDOWN,
            ),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        Button(text="Open on Spotify", url=song.url),
                        Button(text="Add to queue", callback_data="queue;" + song.id),
                    ]
                ]
            ),
        )
    ]

    if status.context:
        thumb = status.context.thumbnail
        if status.context.type == "album":
            title = "{} - {}".format(status.context.artist, status.context.name)
            message_content = "🎧 [{}]({}) by {}".format(
                escape_markdown(status.context.name),
                status.context.url,
                escape_markdown(status.context.artist)
            )
        else:
            title = status.context.name
            message_content = "🎧 [{}]({})".format(
                escape_markdown(status.context.name), status.context.url
            )
        results.append(
            InlineQueryResultArticle(
                id=uuid4(),
                title=title,
                url=status.context.url,
                description=status.context.type,
                thumb_url=thumb.url,
                thumb_width=thumb.width,
                thumb_height=thumb.height,
                input_message_content=InputTextMessageContent(
                    message_content,
                    parse_mode=ParseMode.MARKDOWN,
                ),
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            Button(text="Open on Spotify", url=status.context.url),
                        ]
                    ]
                )
            )
        )

    update.inline_query.answer(results, cache_time=0)


@orm.db_session
def callback_query(update, context):
    query = update.callback_query
    user_id = str(update.effective_user.id)
    command, track_id = query.data.split(";")

    user = User.get(telegram_id=user_id)
    if not user:
        # url = "t.me/" + context.bot.username + "?start=modify_playback_state"
        text = "Please log in by texting /start to {}".format(context.bot.name)
        query.answer(text, show_alert=False)
        return

    try:
        user.spotify.add_to_queue(track_id)
        print("Add to queue " + track_id)
        query.answer("Added to your queue", show_alert=False)
    except AuthError:
        print("Add to queue error " + track_id)
        text = """Authorization needed, please login again.
To do so, text /start to {}""".format(
            context.bot.name
        )
        query.answer(text, show_alert=True)
    except ApiError as e:
        text = "An error occurred"
        if e.msg:
            if "No active device found" in e.msg:
                text = "No active device found"
            if "Restricted device" in e.msg:
                text = "Your device is not supported"
            if "Premium required" in e.msg:
                text = "This requires Spotify Premium"
        query.answer(text, show_alert=False)


def error(update, context):
    """Log Errors caused by Updates."""
    print('Update "%s" caused error "%s"', update, context.error)
