import json
from decouple import config
from telegram import ParseMode
from telegram.ext import Filters, CommandHandler

from dbmodels import Tacos, Chats
from filters import filter_init
from phrases import balance_phrase, balance_comment_medium, balance_comment_high, balance_comment_low,\
    taco_top_phrase, empty_top_phrase
from tools import get_uid, store_name, get_cid, resolve_name

default_taco_amount = config('DEFAULT_TACOS', default=50, cast=int)


def my_tacos_callback(update, _context):
    """ shows users taco-balance """

    cid = get_cid(update)

    store_name(update)

    uid = str(get_uid(update))
    tacos = Tacos.get(Tacos.chat == cid)

    balances = json.loads(tacos.taco_balance)

    if uid in balances.keys():
        balance = balances.get(uid)
    else:
        balances.update({uid: default_taco_amount})
        tacos.taco_balance = json.dumps(balances)
        tacos.save()
        balance = default_taco_amount

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


def taco_top_callback(update, context):
    """ shows top-5(or less) taco-users in chat """

    cid = get_cid(update)
    store_name(update)

    tacos = Tacos.get(Tacos.chat == cid)

    balances = json.loads(tacos.taco_balance)

    if len(balances) == 0:                                                                # in case tacos-table is empty
        update.message.reply_text(empty_top_phrase,
                                  parse_mode=ParseMode.HTML)
        return

    top = list()

    while len(balances) > 0 and len(top) < 5:
        top_uid = max(balances, key=balances.get)
        username = resolve_name(top_uid)
        top.append([username, balances.get(top_uid)])
        del balances[top_uid]

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
