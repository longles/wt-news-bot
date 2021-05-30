# wt-news-bot

Discord bot which scrapes news and patchnotes from [warthunder.com](https://warthunder.com/en)

## Setup

Run `create_db.py` to create the SQLite DB which stores the links
```
python create_db.py
```

Then create an env file called `bot_token.env` with single entry:
```
TOKEN = Enter your bot's token here
```

Afterwards start the bot by running `bot.py`
```
python bot.py
```
