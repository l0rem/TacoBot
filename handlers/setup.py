from telegram import ParseMode
from telegram.error import Unauthorized
from telegram.ext import CommandHandler, MessageHandler, Filters

from dbmodels import Chats, Tacos
from filters import filter_added, filter_self_kicked, filter_invitor
from phrases import new_group_phrase, data_deleted_phrase, \
    chat_enabled_phrase
from tools import get_cid, store_name

default_amount = 50  # default amount of tacos, that every user gets on start


def self_kick_callback(update, context):
    """ if bot gets kicked it erases all data for chat """

    cid = get_cid(update)

    chat = Chats.select().where(Chats.cid == cid)

    if chat.exists():
        chat = chat.get()
        invited_by = chat.invited_by

        tacos = Tacos.select().where(Tacos.chat == chat.id)
        if tacos.exists():
            Tacos.get(Tacos.chat == chat.id).delete_instance()
        chat.delete_instance()

        try:
            chat_title = update.effective_message.chat.title
            context.bot.send_message(invited_by,
                                     data_deleted_phrase.format(chat_title),
                                     parse_mode=ParseMode.HTML)
        except Unauthorized:
            pass  # user deleted bot or didnt /start it


self_kick_handler = MessageHandler(Filters.group & filter_self_kicked,
                                   callback=self_kick_callback)


def init_taco_callback(update, context):
    """ creates Taco-table after permission """

    cid = get_cid(update)

    chat = Chats.get(Chats.cid == cid)
    Tacos.create(chat=chat.id)

    context.bot.send_message(cid,
                             chat_enabled_phrase,
                             parse_mode=ParseMode.HTML)


init_taco_handler = CommandHandler(command='inittaco',
                                   callback=init_taco_callback,
                                   filters=Filters.group & filter_invitor)


def new_chat_callback(update, context):
    """ triggers when bot gets added to new chat """

    cid = get_cid(update)
    store_name(update)

    invited_by = update.effective_message.from_user

    name = store_name(update)

    Chats.create(cid=cid,
                 invited_by=invited_by.id)

    context.bot.send_message(cid,
                             new_group_phrase.format(name),
                             parse_mode=ParseMode.HTML)


new_chat_handler = MessageHandler(Filters.group & filter_added,
                                  callback=new_chat_callback)
