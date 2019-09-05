# TacoBot for Telegram

This is a port of HeyTacoBot (Slack only) for Telegram.

## Installation

This project requires a [Heroku](https://www.heroku.com/) -ish environment. You can also self-host using [Dokku](http://dokku.viewdocs.io/dokku/).

Assuming Dokku, SSH into your _VPS with DOKKU installed_ on it and:
1. `dokku apps:create [APP-NAME]`
2. `dokku config:set --no-restart [APP-NAME] BOT_TOKEN=[YOUR-BOT-TOKEN]`
3. `dokku config:set --no-restart [APP-NAME] WEBHOOK_URL=[YOUR-WEBHOOK-URL]`

From _local machine_:
4. `git init`
5. `git clone git@github.com:l0rem/TacoBot.git`
6. `git remote add dokku dokku@dokku.me:[APP-NAME]`
7. `git push dokku master`

Again _on VPS_:
8. `dokku letsencrypt [APP-NAME]` (requires letsencrypt plugin)
9. `dokku proxy:ports-set [APP-NAME] https:443:8080`

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
