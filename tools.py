from telegram import Update

from dbmodels import Usernames


def get_uid(update: Update):
    """ this makes your life easier """
    return update.effective_message.from_user.id


def get_cid(update: Update):
    """ this makes your life easier """
    return update.effective_message.chat.id


def store_name(update: Update):
    """ this function is here only for /tacotop """

    uid = get_uid(update)

    username = Usernames.select().where(Usernames.uid == uid)
    if username.exists():
        return username.get().name

    user = update.effective_message.from_user
    if user.username is None:
        username = None
        first_name = user.first_name
        last_name = user.last_name
        if last_name is None:
            name = first_name
        else:
            name = first_name + ' ' + last_name
    else:
        name = '@' + user.username
        username = user.username.lower()

    Usernames.create(
        uid=uid,
        name=name,
        username=username)
    return name


def resolve_name(uid):                                                               # returns username if present in DB
    user = Usernames.select().where(Usernames.uid == uid)
    if user.exists():
        return user.get().name
    else:
        return uid


def resolve_uid(username):
    pass  # TODO


def ensure_username(name: str):
    """
    Forces an @ sign to be inserted at the beginning of the passed `name`
    :param name: A telegram username
    """
    return '@' + ensure_no_at_sign(name)


def ensure_no_at_sign(name: str):
    return name.lstrip('@')
