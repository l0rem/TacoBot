from pyrogram import MessageHandler, Filters
from dbmodels import Chats, Tacos, db
from filters import filter_self_kicked, filter_new_chat
from phrases import data_deleted_phrase, chat_enabled_phrase
from chattools import get_cid, store_name


def new_chat_callback(bot, message):
    """ triggers when bot gets added to new chat """

    cid = get_cid(message)
    if message.from_user is not None:
        store_name(message.from_user)

    invited_by = message.from_user

    with db:

        Chats.create(
            cid=cid,
            invited_by=invited_by.id)

        Tacos.create(
            chat=cid)

    bot.send_message(cid,
                     chat_enabled_phrase,
                     parse_mode='html')


new_chat_handler = MessageHandler(callback=new_chat_callback,
                                  filters=Filters.group & ~filter_new_chat & ~filter_self_kicked)


def self_kick_callback(bot, message):
    """ if bot gets kicked it erases all data for chat """

    cid = get_cid(message)

    with db:
        chat = Chats.select().where(Chats.cid == cid)

        if chat.exists():
            chat = chat.get()
            invited_by = chat.invited_by
            chat.delete_instance()

            tacos = Tacos.select().where(Tacos.chat == cid)
            if tacos.exists():
                tacos.get().delete_instance()

            chat_title = message.chat.title

    try:
        bot.send_message(invited_by,
                         data_deleted_phrase.format(chat_title),
                         parse_mode='html')
    except Exception as e:
        """ user blocked the bot """
        print(e)


self_kick_handler = MessageHandler(callback=self_kick_callback,
                                   filters=Filters.group & Filters.left_chat_member & filter_self_kicked)
