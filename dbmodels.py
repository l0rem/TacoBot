from peewee import *
from playhouse.db_url import connect
from decouple import config


db_proxy = Proxy()
db = connect(config("DATABASE_URL", default='sqlite:///tacoDB.sqlite', cast=str), autorollback=True)
db_proxy.initialize(db)


class Chats(Model):                                                        # chats-model is here for future updates only
    cid = BigIntegerField()
    invited_by = BigIntegerField()

    class Meta:
        database = db


if not Chats.table_exists():                                                             # creating chats if not present
    db.create_tables([Chats])


class Tacos(Model):                                                 # taco-model stores balances and chat-related things
    chat = BigIntegerField()
    taco_balance = TextField(null=True,
                             default='{}')

    class Meta:
        database = db


if not Tacos.table_exists():                                                             # creating tacos if not present
    db.create_tables([Tacos])


class Usernames(Model):                                                       # username-model is here only for /tacotop
    uid = BigIntegerField()
    name = CharField()
    username = CharField()

    class Meta:
        database = db


if not Usernames.table_exists():                                                     # creating usernames if not present
    db.create_tables([Usernames])
