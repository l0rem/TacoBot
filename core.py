from telegram.ext import Updater
import logging
from decouple import config
import os

from handlers.basic import help_handler, start_handler
from handlers.leaderboards import taco_top_handler, my_tacos_handler
from handlers.setup import init_taco_handler, self_kick_handler, new_chat_handler
from handlers.tacotransfers import chat_reply_handler

bot_token = config('BOT_TOKEN', default='token')

webhook_url = config('WEBHOOK_URL', default='url')


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',                   # logging > console
                    level=logging.getLevelName(config('LOG_LEVEL', default='DEBUG')))

upd = Updater(bot_token,                                                                   # creating updater/dispatcher
              use_context=True)
dp = upd.dispatcher

if __name__ == '__main__':                                                               # adding handlers to dispatcher
    dp.add_handler(start_handler)
    dp.add_handler(help_handler)
    dp.add_handler(new_chat_handler)
    dp.add_handler(self_kick_handler)
    dp.add_handler(chat_reply_handler)
    dp.add_handler(init_taco_handler)
    dp.add_handler(my_tacos_handler)
    dp.add_handler(taco_top_handler)

    if os.name == 'nt':
        upd.start_polling()
    else:

        upd.start_webhook(listen='0.0.0.0',
                          port=8080,
                          url_path=bot_token)

        upd.bot.set_webhook(webhook_url + bot_token)         # you obviously need to change this url

    logging.info("Ready and listening for updates...")
    upd.idle()

