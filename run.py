import tornado.web

from web_views import urls
from bot_handlers import command_handlers
from utils import updater

def main():

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    for command in command_handlers:
        dp.add_handler(command)

    # Start the Bot
    updater.start_polling()

    app = tornado.web.Application(urls)
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()