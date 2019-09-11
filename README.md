# TacoBot for Telegram

This is a port of HeyTaco Bot (Slack) for Telegram.

## Installation

This project requires a [Heroku](https://www.heroku.com/) -ish environment. You can also self-host using [Dokku](http://dokku.viewdocs.io/dokku/). 
You can obtain `[BOT_TOKEN]` and `[API_ID]/[API_HASH]` for your instance by contacting [@BotFather](https://t.me/botfather) and on [Telegram\'s website](https://my.telegram.org/)

Assuming Dokku, SSH into your _VPS with DOKKU installed_ on it and:
1. `dokku apps:create [APP-NAME]`
2. `dokku config:set --no-restart [APP-NAME] BOT_TOKEN=[YOUR-BOT-TOKEN]`
3. `dokku config:set --no-restart [APP-NAME] API_ID=[YOUR-API_ID]`
4. `dokku config:set --no-restart [APP-NAME] API_HASH=[YOUR-API_HASH]`
5. `dokku postgres:create [DB-NAME]` (requires [postgres plugin](https://github.com/dokku/dokku-postgres))
6. `doku postgres:link [DB-NAME] [APP-NAME]`


From _local machine_:</br>
7. `git init`</br>
8. `git clone git@github.com:l0rem/TacoBot.git`</br>
9. `git remote add dokku dokku@dokku.me:[APP-NAME]`</br>
10. `git push dokku master`

## Usage

Send /start to bot.

Add it to your group and give it admin rights, so that it will be able to access messages.

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## Credits

python-telegram-bot 
DOKKU 
HeyTacoBot
