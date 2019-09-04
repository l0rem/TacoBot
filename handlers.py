from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram.error import Unauthorized
from tools import get_uid, get_cid, store_name, resolve_name
from phrases import start_phrase, help_phrase, new_group_phrase, no_init_phrase, data_deleted_phrase, \
    chat_enabled_phrase, taco_emoji, no_bots_allowed_phrase, self_tacoing_phrase, balance_low_phrase, balance_phrase,\
    balance_comment_high, balance_comment_low, balance_comment_medium, taco_transfer_phrase, \
    taco_transfer_comment_high, taco_transfer_comment_low, taco_transfer_comment_medium, taco_top_phrase,\
    empty_top_phrase
from telegram import ParseMode
from dbmodels import Chats, Tacos
from filters import filter_reply, filter_taco, filter_added, filter_self_kicked, filter_invitor, filter_init
import json
import re


default_amount = 50                                             # default amount of tacos, that every user gets on start


def start_callback(update, context):                                                     # callback for /start (private)
    uid = get_uid(update)

    context.bot.send_message(uid,
                             start_phrase,
                             parse_mode=ParseMode.HTML)


start_handler = CommandHandler('start',
                               callback=start_callback,
                               filters=Filters.private)


def help_callback(update, context):                                                       # callback for /help (private)
    uid = get_uid(update)

    context.bot.send_message(uid,
                             help_phrase,
                             parse_mode=ParseMode.HTML)


help_handler = CommandHandler('help',
                              callback=help_callback,
                              filters=Filters.private)


def chat_reply_callback(update, context):                                                   # callback for taco-transfer
    cid = get_cid(update)
    store_name(update)

    chat = Chats.get(Chats.cid == cid)
    tacos = Tacos.select().where(Tacos.chat == chat.id)
    if not tacos.exists():
        context.bot.send_message(cid,
                                 no_init_phrase,
                                 parse_mode=ParseMode.HTML)
        return

    tacos = Tacos.get(Tacos.chat == chat.id)

    sender = update.effective_message.from_user                                                # finding sender/receiver
    receiver = update.effective_message.reply_to_message.from_user

    if receiver.username is None:
        first_name = receiver.first_name
        last_name = receiver.last_name
        if last_name is None:
            receiver_name = first_name
        else:
            receiver_name = first_name + ' ' + last_name
    else:
        receiver_name = '@' + receiver.username

    if receiver.is_bot:                                                                              # no tacos for bots
        update.message.reply_text(no_bots_allowed_phrase,
                                  parse_mode=ParseMode.HTML)
        return

    sender_id = str(sender.id)
    receiver_id = str(receiver.id)

    if sender_id == receiver_id:                                                             # self-tacoing is forbidden
        update.message.reply_text(self_tacoing_phrase,
                                  parse_mode=ParseMode.HTML)
        return

    tacos_sent = len(re.findall('{}'.format(taco_emoji), update.effective_message.text))                # counting tacos

    if tacos.taco_balance is None:                                                # initialising/restoring user-balances
        amounts = dict()
        amounts.update({sender_id: default_amount})
        amounts.update({receiver_id: default_amount})
    else:
        amounts = json.loads(tacos.taco_balance)
        if sender_id not in amounts.keys():
            amounts.update({sender_id: default_amount})
        if receiver_id not in amounts.keys():
            amounts.update({receiver_id: default_amount})

    if tacos_sent > amounts.get(sender_id):                                              # can't send more than you have
        update.message.reply_text(balance_low_phrase,
                                  parse_mode=ParseMode.HTML)
        return

    amounts.update({sender_id: amounts.get(sender_id) - tacos_sent})                              # actual taco-transfer
    amounts.update({receiver_id: amounts.get(receiver_id) + tacos_sent})

    if tacos_sent < 3:
        comment = taco_transfer_comment_low
    elif tacos_sent > 9:
        comment = taco_transfer_comment_high
    else:
        comment = taco_transfer_comment_medium.format(receiver_name)

    update.message.reply_text(taco_transfer_phrase.format(tacos_sent,
                                                          receiver_name,
                                                          comment),
                              parse_mode=ParseMode.HTML)

    tacos.taco_balance = json.dumps(amounts)                                                               # saving data
    tacos.save()


chat_reply_handler = MessageHandler(callback=chat_reply_callback,
                                    filters=Filters.group & filter_reply & filter_taco)


def new_chat_callback(update, context):                                       # triggers when bot gets added to new chat
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


def self_kick_callback(update, context):                                # if bot gets kicked it erases all data for chat
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
            pass                                                                   # user deleted bot or didnt /start it


self_kick_handler = MessageHandler(Filters.group & filter_self_kicked,
                                   callback=self_kick_callback)


def init_taco_callback(update, context):                                           # creates Taco-table after permission
    cid = get_cid(update)

    chat = Chats.get(Chats.cid == cid)
    Tacos.create(chat=chat.id)

    context.bot.send_message(cid,
                             chat_enabled_phrase,
                             parse_mode=ParseMode.HTML)


init_taco_handler = CommandHandler(command='inittaco',
                                   callback=init_taco_callback,
                                   filters=Filters.group & filter_invitor)


def my_tacos_callback(update, context):                                                       # shows users taco-balance
    cid = get_cid(update)
    chat = Chats.get(Chats.cid == cid)
    store_name(update)

    uid = str(get_uid(update))
    tacos = Tacos.get(Tacos.chat == chat.id)

    balances = json.loads(tacos.taco_balance)

    if uid in balances.keys():
        balance = balances.get(uid)
    else:
        balances.update({uid: default_amount})
        tacos.taco_balance = json.dumps(balances)
        tacos.save()
        balance = default_amount

    if balance < 25:
        comment = balance_comment_low
    elif balance > 60:
        comment = balance_comment_high
    else:
        comment = balance_comment_medium

    update.message.reply_text(balance_phrase.format(balance,
                                                    comment),
                              parse_mode=ParseMode.HTML)


my_tacos_handler = CommandHandler(command='mytacos',
                                  callback=my_tacos_callback,
                                  filters=Filters.group & filter_init)


def taco_top_callback(update, context):                                        # shows top-5(or less) taco-users in chat
    cid = get_cid(update)
    store_name(update)

    chat = Chats.get(Chats.cid == cid)
    tacos = Tacos.get(Tacos.chat == chat.id)

    b = json.loads(tacos.taco_balance)

    if len(b) == 0:                                                                       # in case tacos-table is empty
        update.message.reply_text(empty_top_phrase,
                                  parse_mode=ParseMode.HTML)
        return

    balances = list()
    for balance in b.keys():
        balances.append([balance, b.get(balance)])

    top = list()

    while len(balances) > 0 and len(top) < 5:                                                  # classical sort by value
        mx_value = -1
        for k in range(len(balances)):
            if balances[k][1] >= mx_value:
                mx_user = k
        top.append(balances[mx_user])
        del balances[mx_user]

    for user in top:                                                                 # resolving usernames for top-table
        user[0] = resolve_name(user[0])

    formatted_top = ''
    for user in top:
        formatted_top += '{}. {} - <code>{}</code> tacos!\n'.format(top.index(user) + 1,
                                                                    user[0],
                                                                    user[1])

    update.message.reply_text(taco_top_phrase.format(len(top),
                                                     formatted_top),
                              parse_mode=ParseMode.HTML)


taco_top_handler = CommandHandler(command='tacotop',
                                  callback=taco_top_callback,
                                  filters=Filters.group & filter_init)
