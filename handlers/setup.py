from telegram import ParseMode
from telegram.error import Unauthorized
from telegram.ext import MessageHandler, Filters

from dbmodels import Chats, Tacos
from filters import filter_self_kicked, filter_new_chat
from phrases import data_deleted_phrase, chat_enabled_phrase
from tools import get_cid, store_name


def new_chat_callback(update, context):
    """ triggers when bot gets added to new chat """

    cid = get_cid(update)
    store_name(update)

    invited_by = update.effective_message.from_user

    Chats.create(cid=cid,
                 invited_by=invited_by.id)

    Tacos.create(chat=cid)

    context.bot.send_message(cid,
                             chat_enabled_phrase,
                             parse_mode=ParseMode.HTML)


new_chat_handler = MessageHandler(Filters.group & filter_new_chat & ~filter_self_kicked,
                                  callback=new_chat_callback)


def self_kick_callback(update, context):
    """ if bot gets kicked it erases all data for chat """

    cid = get_cid(update)

    chat = Chats.select().where(Chats.cid == cid)
    if chat.exists():
        chat = chat.get()
        invited_by = chat.invited_by
        chat.delete_instance()

        tacos = Tacos.select().where(Tacos.chat == cid)
        if tacos.exists():
            tacos.get().delete_instance()

        try:
            chat_title = update.effective_message.chat.title
            context.bot.send_message(invited_by,
                                     data_deleted_phrase.format(chat_title),
                                     parse_mode=ParseMode.HTML)
        except Unauthorized:
            pass  # user deleted bot or didnt /start it


self_kick_handler = MessageHandler(Filters.group & filter_self_kicked,
                                   callback=self_kick_callback)
