import json
import re
from typing import List, Dict, Union
from decouple import config
from peewee import fn
from peewee import DoesNotExist
from telegram import ParseMode, MessageEntity, Update, Message, User, ChatMember
from telegram.ext import Filters, MessageHandler, CallbackContext

from dbmodels import Tacos, Chats, Usernames
from filters import filter_taco, filter_reply
from phrases import (
    taco_transfer_phrase,
    taco_transfer_comment_medium,
    taco_transfer_comment_high,
    taco_transfer_comment_low,
    balance_low_phrase,
    taco_emoji,
    self_tacoing_phrase,
    no_bots_allowed_phrase,
    only_one_receiver_phrase,
    user_not_present_phrase
)
from tacotools import count_tacos
from tools import store_name, get_cid, ensure_no_at_sign, ensure_username

default_taco_amount = config('DEFAULT_TACOS', default=50, cast=int)


def give_tacos(update: Update, sender: User, receiver: Union[User, ChatMember], amount: int):
    receiver: User = receiver.user if isinstance(receiver, ChatMember) else receiver
    cid = get_cid(update)

    tacos = Tacos.get(Tacos.chat == cid)

    if receiver.username is None:
        first_name = receiver.first_name
        last_name = receiver.last_name
        if last_name is None:
            receiver_name = first_name
        else:
            receiver_name = first_name + " " + last_name
    else:
        receiver_name = "@" + receiver.username

    if receiver.is_bot:  # no tacos for bots
        update.message.reply_text(no_bots_allowed_phrase, parse_mode=ParseMode.HTML)
        return

    sender_id = str(sender.id)
    receiver_id = str(receiver.id)

    if sender_id == receiver_id:  # self-tacoing is forbidden
        update.message.reply_text(self_tacoing_phrase, parse_mode=ParseMode.HTML)
        return

    tacos_sent = len(
        re.findall(taco_emoji, update.effective_message.text)
    )

    if tacos.taco_balance is None:  # initialising/restoring user-balances
        amounts = dict()
        amounts.update({sender_id: amount})
        amounts.update({receiver_id: amount})
    else:
        amounts = json.loads(tacos.taco_balance)
        if sender_id not in amounts.keys():
            amounts.update({sender_id: amount})
        if receiver_id not in amounts.keys():
            amounts.update({receiver_id: amount})

    if tacos_sent > amounts.get(sender_id):  # can't send more than you have
        update.message.reply_text(balance_low_phrase, parse_mode=ParseMode.HTML)
        return

    amounts.update(
        {sender_id: amounts.get(sender_id) - tacos_sent}
    )
    amounts.update({receiver_id: amounts.get(receiver_id) + tacos_sent})

    if tacos_sent < 3:
        comment = taco_transfer_comment_low
    elif tacos_sent > 9:
        comment = taco_transfer_comment_high
    else:
        comment = taco_transfer_comment_medium.format(receiver_name)

    update.message.reply_text(
        taco_transfer_phrase.format(tacos_sent, receiver_name, comment),
        parse_mode=ParseMode.HTML,
    )

    tacos.taco_balance = json.dumps(amounts)  # saving data
    tacos.save()


def chat_reply_callback(update: Update, context: CallbackContext):
    """ callback for taco-transfer """

    store_name(update)

    sender: User = update.effective_message.from_user
    receiver: User = update.effective_message.reply_to_message.from_user

    give_tacos(update, sender, receiver, default_taco_amount)


chat_reply_handler = MessageHandler(
    callback=chat_reply_callback, filters=Filters.group & filter_reply & filter_taco
)


def taco_mention_callback(update: Update, context: CallbackContext):
    """ callback for taco-transfer by mention """

    cid = get_cid(update)
    store_name(update)

    message: Message = update.message
    mentions: Dict[MessageEntity, str] = message.parse_entities(
        [MessageEntity.MENTION, MessageEntity.TEXT_MENTION]
    )
    mentioned_users: List[str] = [m.lower() for m in mentions.values()]

    mentioned_users = list(set(mentioned_users))   # removing duplicates

    if len(mentioned_users) > 1:

        update.message.reply_text(
            only_one_receiver_phrase,
            parse_mode=ParseMode.HTML
        )
        return

    sender: User = update.effective_message.from_user
    receiver_username: str = ensure_no_at_sign(mentioned_users[0])
    amount = count_tacos(message)

    try:
        receiver_db_entity: Usernames = Usernames.select().where(fn.lower(Usernames.username) == receiver_username).get()
        # TODO resolve_uid(username)
        receiver: User = context.bot.get_chat_member(cid, receiver_db_entity.uid)
        give_tacos(update, sender, receiver, amount)
    except DoesNotExist:

        update.message.reply_text(user_not_present_phrase.format(ensure_username(receiver_username)),
                                  parse_mode=ParseMode.HTML)


taco_mention_handler = MessageHandler(
    callback=taco_mention_callback,
    filters=Filters.group
    & filter_taco
    & (
        Filters.entity(MessageEntity.MENTION)
        | Filters.entity(MessageEntity.TEXT_MENTION)
    ),
)
