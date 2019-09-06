from telegram.ext import Updater
import logging
from decouple import config
from handlers.basic import help_handler, start_handler, store_names_handler
from handlers.leaderboards import taco_top_handler, my_tacos_handler
from handlers.setup import self_kick_handler, new_chat_handler
from handlers.tacotransfers import chat_reply_handler, taco_mention_handler

env = config('ENV', default='DEV')

bot_token = config('BOT_TOKEN', default='token')

webhook_url = config('WEBHOOK_URL', default='url')


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.getLevelName(config('LOG_LEVEL', default='DEBUG')))

upd = Updater(bot_token,
              use_context=True)
dp = upd.dispatcher

if __name__ == '__main__':
    # Always execute these first, synchronously
    dp.add_handler(new_chat_handler, group=-1)
    dp.add_handler(store_names_handler, group=-1)

    dp.add_handler(start_handler)
    dp.add_handler(help_handler)
    dp.add_handler(self_kick_handler)
    dp.add_handler(chat_reply_handler)
    dp.add_handler(my_tacos_handler)
    dp.add_handler(taco_top_handler)
    dp.add_handler(taco_mention_handler)

    if env == 'DEV':
        upd.start_polling()
    else:

        upd.start_webhook(listen='0.0.0.0',
                          port=8080,
                          url_path=bot_token)

        upd.bot.set_webhook(webhook_url + bot_token)


    logging.info("Ready and listening for updates...")
    upd.idle()

