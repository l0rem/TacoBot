from peewee import *

db = SqliteDatabase('taco_base.db')                                                                # opening/creating DB


class Chats(Model):                                                        # chats-model is here for future updates only
    cid = IntegerField()
    invited_by = IntegerField()

    class Meta:
        database = db


if not Chats.table_exists():                                                             # creating chats if not present
    db.create_tables([Chats])


class Tacos(Model):                                                 # taco-model stores balances and chat-related things
    chat = IntegerField()
    taco_balance = TextField(null=True,
                             default='{}')

    class Meta:
        database = db


if not Tacos.table_exists():                                                             # creating tacos if not present
    db.create_tables([Tacos])


class Usernames(Model):                                                       # username-model is here only for /tacotop
    uid = IntegerField()
    name = CharField()
    username = CharField()

    class Meta:
        database = db


if not Usernames.table_exists():                                                     # creating usernames if not present
    db.create_tables([Usernames])
