import json
import re
from typing import List

from telegram import ParseMode, MessageEntity, Update, Message, User
from telegram.ext import Filters, MessageHandler, CallbackContext

from dbmodels import Tacos, Chats
from filters import filter_taco, filter_reply
from handlers.setup import default_amount
from phrases import (
    taco_transfer_phrase,
    taco_transfer_comment_medium,
    taco_transfer_comment_high,
    taco_transfer_comment_low,
    balance_low_phrase,
    taco_emoji,
    self_tacoing_phrase,
    no_bots_allowed_phrase,
    no_init_phrase,
)
from tools import store_name, get_cid


def chat_reply_callback(update, context):
    """ callback for taco-transfer """

    cid = get_cid(update)
    store_name(update)

    chat = Chats.get(Chats.cid == cid)
    tacos = Tacos.select().where(Tacos.chat == chat.id)
    if not tacos.exists():
        context.bot.send_message(cid, no_init_phrase, parse_mode=ParseMode.HTML)
        return

    tacos = Tacos.get(Tacos.chat == chat.id)

    sender = update.effective_message.from_user  # finding sender/receiver
    receiver = update.effective_message.reply_to_message.from_user

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
        re.findall("{}".format(taco_emoji), update.effective_message.text)
    )  # counting tacos

    if tacos.taco_balance is None:  # initialising/restoring user-balances
        amounts = dict()
        amounts.update({sender_id: default_amount})
        amounts.update({receiver_id: default_amount})
    else:
        amounts = json.loads(tacos.taco_balance)
        if sender_id not in amounts.keys():
            amounts.update({sender_id: default_amount})
        if receiver_id not in amounts.keys():
            amounts.update({receiver_id: default_amount})

    if tacos_sent > amounts.get(sender_id):  # can't send more than you have
        update.message.reply_text(balance_low_phrase, parse_mode=ParseMode.HTML)
        return

    amounts.update(
        {sender_id: amounts.get(sender_id) - tacos_sent}
    )  # actual taco-transfer
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


chat_reply_handler = MessageHandler(
    callback=chat_reply_callback, filters=Filters.group & filter_reply & filter_taco
)


def taco_mention_callback(update: Update, context: CallbackContext):
    """ callback for taco-transfer by mention """
    print("taco transfer")

    cid = get_cid(update)
    store_name(update)

    message: Message = update.message
    mentions: List[MessageEntity] = message.parse_entities(
        [MessageEntity.MENTION, MessageEntity.TEXT_MENTION]
    )
    mentioned_users: List[User] = [m.user for m in mentions]

    if len(mentioned_users) > 1:
        # TODO: factor out string
        update.message.reply_text(
            "Sorry, you can only give tacos to <b>one</b> person."
        )


taco_mention_handler = MessageHandler(
    callback=taco_mention_callback,
    filters=Filters.group
    # filters=Filters.group
    # & filter_taco
    # & (
    #     Filters.entity(MessageEntity.MENTION)
    #     | Filters.entity(MessageEntity.TEXT_MENTION)
    # )
)
