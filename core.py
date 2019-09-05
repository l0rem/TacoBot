from telegram.ext import Updater
import logging
from decouple import config
import os

from handlers.basic import help_handler, start_handler, store_names_handler
from handlers.leaderboards import taco_top_handler, my_tacos_handler
from handlers.setup import init_taco_handler, self_kick_handler, new_chat_handler
from handlers.tacotransfers import chat_reply_handler, taco_mention_handler

bot_token = config('BOT_TOKEN', default='token')

webhook_url = config('WEBHOOK_URL', default='url')

env = config('ENV', default='dev')


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',                   # logging > console
                    level=logging.getLevelName(config('LOG_LEVEL', default='DEBUG')))

upd = Updater(bot_token,                                                                   # creating updater/dispatcher
              use_context=True)
dp = upd.dispatcher

if __name__ == '__main__':                                                               # adding handlers to dispatcher
    # Always execute first, synchronously
    dp.add_handler(store_names_handler, group=-1)

    dp.add_handler(start_handler)
    dp.add_handler(help_handler)
    dp.add_handler(new_chat_handler)
    dp.add_handler(self_kick_handler)
    dp.add_handler(chat_reply_handler)
    dp.add_handler(init_taco_handler)
    dp.add_handler(my_tacos_handler)
    dp.add_handler(taco_top_handler)
    dp.add_handler(taco_mention_handler)

    if env == 'dev':
        upd.start_polling()
    else:

        upd.start_webhook(listen='0.0.0.0',
                          port=8080,
                          url_path=bot_token)

        upd.bot.set_webhook(webhook_url + bot_token)         

    logging.info("Ready and listening for updates...")
    upd.idle()

