from pyrogram import MessageHandler, Filters
from phrases import start_phrase, help_phrase, delete_message_fail_phrase, admins_only_phrase,\
    silenced_mode_off_phrase, silenced_mode_on_phrase, autohide_on_phrase, autohide_off_phrase,\
    autohide_delay_set_phrase, autohide_delay_wrong_value_phrase
from dbmodels import Chats, db
from pyrogram import CallbackQueryHandler
from chattools import get_uid, store_name, clean_chat
import json


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
    if message.from_user is not None:
        store_name(message.from_user)


store_names_handler = MessageHandler(callback=store_names_callback)


def less_callback(bot, message):
    with db:
        chat = Chats.get(Chats.cid == message.chat.id)

    clean_chat(chat.mids, chat.cid, bot, message)

    user = bot.get_chat_member(chat_id=message.chat.id,
                               user_id=message.from_user.id)

    if message.from_user.id == chat.invited_by or\
            user.status == 'administrator' or\
            user.status == 'creator':
        if chat.less is False:
            text = silenced_mode_on_phrase
            chat.less = True
        else:
            chat.less = False
            text = silenced_mode_off_phrase
        mid = bot.send_message(chat_id=chat.cid,
                               text=text,
                               parse_mode='html').message_id
        chat.mids = json.dumps([mid])
        with db:
            chat.save()
    else:
        text = admins_only_phrase
        mid = bot.send_message(chat_id=chat.cid,
                               text=text,
                               parse_mode='html').message_id
        chat.mids = json.dumps([mid])
        with db:
            chat.save()



less_handler = MessageHandler(callback=less_callback,
                              filters=Filters.command('tacosilence') & Filters.group)


def autohide_callback(bot, message):
    with db:
        chat = Chats.get(Chats.cid == message.chat.id)
    clean_chat(chat.mids, chat.cid, bot, message)

    user = bot.get_chat_member(chat_id=message.chat.id,
                               user_id=message.from_user.id)

    if message.from_user.id == chat.invited_by or\
            user.status == 'administrator' or\
            user.status == 'creator':

        if chat.autohide is False:
            text = autohide_on_phrase
            chat.autohide = True

        else:
            chat.autohide = False
            text = autohide_off_phrase

        mid = bot.send_message(chat_id=chat.cid,
                               text=text,
                               parse_mode='html').message_id

        chat.mids = json.dumps([mid])
        with db:
            chat.save()

    else:
        text = admins_only_phrase

        mid = bot.send_message(chat_id=chat.cid,
                               text=text,
                               parse_mode='html').message_id

        chat.mids = json.dumps([mid])
        with db:
            chat.save()


autohide_handler = MessageHandler(callback=autohide_callback,
                                  filters=Filters.command('autohide_mode') & Filters.group)


def autohide_delay_callback(bot, message):
    with db:
        chat = Chats.get(Chats.cid == message.chat.id)

    clean_chat(chat.mids, chat.cid, bot, message)

    user = bot.get_chat_member(chat_id=message.chat.id,
                               user_id=message.from_user.id)

    if message.from_user.id == chat.invited_by or\
            user.status == 'administrator' or\
            user.status == 'creator':

        if (args := len(message.command)) == 1:
            delay = 15
        elif args > 2:
            bot.send_message(chat_id=chat.cid,
                             text=autohide_delay_wrong_value_phrase,
                             parse_mode='html')
            return
        else:
            try:
                delay = int(message.command[1])
            except ValueError:
                bot.send_message(chat_id=chat.cid,
                                 text=autohide_delay_wrong_value_phrase,
                                 parse_mode='html')
                return

        if delay < 1 or delay > 120:
            bot.send_message(chat_id=chat.cid,
                             text=autohide_delay_wrong_value_phrase,
                             parse_mode='html')
            return

        chat.autohide_delay = delay

        mid = bot.send_message(chat_id=chat.cid,
                               text=autohide_delay_set_phrase.format(delay),
                               parse_mode='html').message_id

        chat.mids = json.dumps([mid])
        with db:
            chat.save()

    else:
        text = admins_only_phrase

        mid = bot.send_message(chat_id=chat.cid,
                               text=text,
                               parse_mode='html').message_id

        chat.mids = json.dumps([mid])
        with db:
            chat.save()


autohide_delay_handler = MessageHandler(callback=autohide_delay_callback,
                                        filters=Filters.command('autohide_delay') & Filters.group)


def delete_callback(bot, callbackquery):
    data = callbackquery.data
    user = bot.get_chat_member(chat_id=callbackquery.message.chat.id,
                               user_id=callbackquery.from_user.id)

    if int(data.split(':')[1]) == callbackquery.from_user.id or\
            user.status == 'administrator' or\
            user.status == 'creator':
        try:
            bot.delete_messages(chat_id=callbackquery.message.chat.id,
                                message_ids=callbackquery.message.message_id)
        except Exception as e:
            print(e)
            pass
    else:
        bot.answer_callback_query(callback_query_id=callbackquery.id,
                                  text=delete_message_fail_phrase)


delete_handler = CallbackQueryHandler(filters=Filters.callback_data,
                                      callback=delete_callback)


def delete_message(bot, message):
    try:
        bot.delete_messages(chat_id=message.chat.id,
                            message_ids=message.message_id)
    except Exception as e:
        print(e)
        pass
