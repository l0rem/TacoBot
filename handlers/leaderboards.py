import json

from telegram import ParseMode
from telegram.ext import Filters, CommandHandler

from dbmodels import Tacos, Chats
from filters import filter_init
from handlers.setup import default_amount
from phrases import balance_phrase, balance_comment_medium, balance_comment_high, balance_comment_low, taco_top_phrase, \
    empty_top_phrase
from tools import get_uid, store_name, get_cid, resolve_name


def my_tacos_callback(update, _context):
    """ shows users taco-balance """

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


def taco_top_callback(update, context_):
    """ shows top-5(or less) taco-users in chat """

    cid = get_cid(update)
    store_name(update)

    chat = Chats.get(Chats.cid == cid)
    tacos = Tacos.get(Tacos.chat == chat.id)

    b = json.loads(tacos.taco_balance)

    if len(b) == 0:  # in case tacos-table is empty
        update.message.reply_text(empty_top_phrase,
                                  parse_mode=ParseMode.HTML)
        return

    balances = list()
    for balance in b.keys():
        balances.append([balance, b.get(balance)])

    top = list()

    while len(balances) > 0 and len(top) < 5:  # classical sort by value
        mx_value = -1
        # TODO: mx_user might be reference before assignment
        for k in range(len(balances)):
            if balances[k][1] >= mx_value:
                mx_user = k
        top.append(balances[mx_user])
        del balances[mx_user]

    for user in top:  # resolving usernames for top-table
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
