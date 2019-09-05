from telegram import ParseMode
from telegram.ext import Filters, CommandHandler

from phrases import start_phrase, help_phrase
from tools import get_uid


def start_callback(update, context):
    """ callback for /start (private) """

    uid = get_uid(update)

    context.bot.send_message(uid,
                             start_phrase,
                             parse_mode=ParseMode.HTML)


start_handler = CommandHandler('start',
                               callback=start_callback,
                               filters=Filters.private)


def help_callback(update, context):
    """ callback for /help (private) """

    uid = get_uid(update)

    context.bot.send_message(uid,
                             help_phrase,
                             parse_mode=ParseMode.HTML)


help_handler = CommandHandler('help',
                              callback=help_callback,
                              filters=Filters.private)
