import tornado.web

from web_views import urls
from bot_handlers import handlers
from utils import updater, app_port
import logging

logging.basicConfig(level=logging.INFO)


def main():

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    for command in handlers:
        dp.add_handler(command)

    # Start the Bot
    updater.start_polling()

    app = tornado.web.Application(urls)
    app.listen(app_port)

    print("Bot is running!")

    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
