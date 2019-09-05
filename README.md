# TacoBot for Telegram

This is a port of HeyTacoBot (Slack only) for Telegram.

## Installation

SSH into your VPS with DOKKU installed on it:
1. dokku apps:create [APP-NAME]
2. dokku config:set --no-restart [APP-NAME] BOT_TOKEN=[YOUR-BOT-TOKEN]
3. dokku config:set --no-restart [APP-NAME] WEBHOOK_URL=[YOUR-WEBHOOK-URL]
4. dokku buildpacks:add [APP-NAME]  https://github.com/heroku/heroku-buildpack-python.git
5. git clone git@github.com:l0rem/TacoBot.git
6. git push dokku master
6. dokku letsencrypt [APP-NAME]

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
