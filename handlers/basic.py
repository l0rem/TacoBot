from pyrogram import MessageHandler, Filters
from phrases import start_phrase, help_phrase
from chattools import get_uid, store_name


def start_callback(bot, message):
    """ callback for /start (private) """
    uid = get_uid(message)

    bot.send_message(uid,
                     start_phrase,
                     parse_mode='html')


start_handler = MessageHandler(callback=start_callback,
                               filters=Filters.command('start') & Filters.private)


def help_callback(bot, message):
    """ callback for /help (private) """
    uid = get_uid(message)

    bot.send_message(uid,
                     help_phrase,
                     parse_mode='html')


help_handler = MessageHandler(callback=help_callback,
                              filters=Filters.private)


def store_names_callback(bot, message):
    """ stores names for each user, if not already present in DB"""
    store_name(message)


store_names_handler = MessageHandler(callback=store_names_callback)
