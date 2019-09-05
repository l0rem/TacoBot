from typing import Union

from telegram import Message

from phrases import taco_emoji


def count_tacos(msg: Union[str, Message]) -> int:
    """ Counts number of taco emojis in a `telegram.Message` or string """
    text = msg.text if isinstance(msg, Message) else msg
    return text.count(taco_emoji)
