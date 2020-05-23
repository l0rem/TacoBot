from decouple import config
from pyrogram import Filters
from dbmodels import Chats, db
from phrases import taco_emoji
from chattools import ensure_username, get_cid

bot_username = ensure_username(config('BOT_USERNAME', default='HeyTacoBot'))


def filter_taco_(_, query):                                                           # filter for taco-emoji in message
    if query.text is not None:
        return taco_emoji in query.text
    return False


filter_taco = Filters.create(filter_taco_)


def filter_self_kicked_(_, query):                                    # filter for update, that bot was kicked from chat
    if query.left_chat_member is None:
        return False
    if ensure_username(query.left_chat_member.username).lower() == bot_username.lower():
        return True
    return False


filter_self_kicked = Filters.create(filter_self_kicked_)


def filter_new_chat_(_, query):                                           # filter for group, that has tacos-field in DB
    with db:
        return Chats.select().where(Chats.cid == get_cid(query)).exists()


filter_new_chat = Filters.create(filter_new_chat_)


def filter_mention_(_, query):  # filter for mention in text message
    if query.entities is None:
        return False
    for entity in query.entities:
        if entity.type == 'mention':
            return True
    return False


filter_mention = Filters.create(filter_mention_)

