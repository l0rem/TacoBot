from decouple import config


default_taco_amount = config('DEFAULT_TACOS', default=50, cast=int)

taco_emoji = '\U0001F32E'

start_phrase = '<b>Hello, my name is TacoBot and my sole purpose is to help you spread appreciation, celebrate, and' \
               ' have a little fun.</b>\n\nSimply add me to your group and you’ll be giving tacos in no time! You can' \
               ' also send me /help to read about my abilities :^)'

help_phrase = '<b>This is what i can do now:</b>\n\n/tacotop - <code>shows top-5 Taco\'ers in current chat (only' \
              ' in groups)</code>\n\n/mytacos - <code>shows your taco-balance (only in groups)</code>\n\nKicking ' \
              'me from group will erase all taco-data for chat. That\'s because i can\'t forgive such a' \
              ' betrayal !!'

new_group_phrase = '<b>Sup, chat!</b>\n\nThanks for adding me :3 You can find out more about my functions by' \
                   ' contacting me in private.\nNow the person that added me ({}) needs to send /inittaco in order to' \
                   ' allow me to work with this group.\n\n<code>P.S. Don\'t forget to give me admin rights, so that I' \
                   ' will be able to access messages and count tacos for you</code>\U00002764'

no_init_phrase = '<b>This chat is not enabled for me!</b>\n\nUser, who invited me, needs to send /inittaco , in order' \
                 ' to allow me counting tacos for this chat.'

data_deleted_phrase = '<b>I got kicked from {}, so data about user\'s tacos got deleted!</b>\n\nHuge thanks for' \
                      ' having me in your chat - feel free to add me again later.'

chat_enabled_phrase = '<b>Thanks!</b>\n\nFrom this moment I\'m counting <i> all </i> tacos for <i> all </i> members' \
                      ' in this chat. You can share tacos by replying to other user\'s messages with taco-emoji' \
                      ' ({}) or by mentioning user(@username) in a message with taco.\n<b>Every user gets</b>' \
                      '<code> {} <b>tacos.</b>\n\n{}\n\n<code>P.S. Again, only if you gave me access to' \
                      ' messages</code>\U00002764'.format(taco_emoji,
                                                          default_taco_amount,
                                                          help_phrase)

no_bots_allowed_phrase = '<b>Sorry, but bots can\'t receive your tacos :(</b>\n\nI don\'t even think, that they can eat' \
                         ' human-food yet \U0001F914\U0001F914\U0001F914'

self_tacoing_phrase = '<b>Why would you want to send these delicious tacos to yourself?..</b>\n\nYou are a' \
                      ' really weird person \U0001F610'

balance_low_phrase = '<b>Whoops... You ran out of tacos!</b>\n\nYou can probably start some crowdfunding page to get' \
                     ' some tacos from your friends and other participants \U0001F643'

balance_phrase = '<b>You have</b> <code>{}</code> <b>tacos on your taco-balance.</b>\n\n{}'

balance_comment_low = 'Where did all your tacos go?!! \U0001F47F\U0001F47F\U0001F47F'

balance_comment_medium = 'I guess, you dont gift much of your tacos... and so do your neighbours \U0001F62A'

balance_comment_high = 'WoW, I\'m impressed! How did you earn so many tacos? Are you trading crypto or what?\U0001F640'

taco_transfer_phrase = '<b>Gave</b> <code>{}</code> <b>tacos to</b> {}<b>!</b>\n\n{}'

taco_transfer_comment_low = 'Why didn\'t you share more tacos tho?\U0001F634'

taco_transfer_comment_medium = '{} must be a good person! \U0001F63D'

taco_transfer_comment_high = 'Do you owe him lots of money or what? \U0001F639'

taco_top_phrase = '<b>Here are the top-{} tacoers in this chat!</b>\n\n{}'

empty_top_phrase = '<b>Omg, there are no taco-lovers in this group!\U0001F47A\U0001F47A\U0001F47A</b>\n\nGo ahead and' \
                   ' reply to someone\'s message with {} ASAP!!!!'.format(taco_emoji)

only_one_receiver_phrase = '<b>Sorry, but there can be only one taco-receiver \U0001F61B</b>\n\nWhy not to split this' \
                           ' into two separate taco-transactions? \U0001F914'

user_not_present_phrase = '<b>Hmm, does </b>{}<b> even exist?</b>\n\nCould (s)he send a message in this chat, so that' \
                          ' we can shake our virtual hands? \U0001F917'

