from decouple import config
from telegram import Message
from telegram.ext import BaseFilter
from dbmodels import Chats, Tacos
from phrases import taco_emoji
from tools import ensure_username

bot_username = ensure_username(config('BOT_USERNAME', default='TacoBot'))

class FilterReply(BaseFilter):                                                                      # filter for replies
    def filter(self, message):
        return message.reply_to_message is not None


filter_reply = FilterReply()


class FilterTaco(BaseFilter):                                                         # filter for taco-emoji in message
    def filter(self, message: Message):
        return taco_emoji in message.text if message.text else False


filter_taco = FilterTaco()


class FilterAdded(BaseFilter):                                         # filter for message, that bot was added to group
    def filter(self, message):
        for member in message.new_chat_members:
            if ensure_username(member.username).lower() == bot_username.lower():
                return True
        return False


filter_added = FilterAdded()


class FilterSelfKicked(BaseFilter):                                   # filter for update, that bot was kicked from chat
    def filter(self, message):
        if message.left_chat_member is None:
            return False
        if ensure_username(message.left_chat_member.username) == bot_username:
            return True
        return False


filter_self_kicked = FilterSelfKicked()


class FilterInvitor(BaseFilter):                               # filter for message, that comes from invitor (/inittaco)
    def filter(self, message):
        if message.from_user.id == Chats.get(Chats.cid == message.chat_id).invited_by:
            return True
        return False


filter_invitor = FilterInvitor()


class FilterInit(BaseFilter):                                             # filter for group, that has tacos-field in DB
    def filter(self, message):
        chat = Chats.get(Chats.cid == message.chat.id)
        tacos = Tacos.select(Tacos.chat == chat.id)
        return tacos.exists()


filter_init = FilterInit()
