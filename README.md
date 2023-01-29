# Woodpecker

Rolling collection of automations for dealing with threat actor use of Telegram. Python, built on Pyrogram. 

# Setup

Fill in fields in the config.ini file. You will need a [Telegram API hash and ID](https://core.telegram.org/api/obtaining_api_id) to engage with the Telegram API. Beware interacting with malicious infrastructure on personal accounts.

# Features

## Phishing related

Phishing kits commonly use Telegram bots as a method of exfiltrating credentials, as an alternative to a PHP mailer or file-based credential log. Phishing kits using Telegram bots will disclose the threat actor's Telegram bot token, which gives any bearer full control of the bot via the Telegram API.

Telegram bots have access to only a subset of the API commands available to a normal account. Despite this, the bot API exposes some powerful commands that can be used to obtain and manipulate messages and potentially wipe the bot. 

Telegram bot tokens can be found in kits with the regular expression `[0-9]{8,10}:[a-zA-Z0-9_-]{35}`. If you find a bot token, you will almost certainly find a chat ID in the same file with the regular expression `[0-9]{9,12}`.  

### Dump messages from Telegram bots used for phishing 

- `python3 woodpecker.py -b [bot_token] -c [chat_id]`
	- Iterate all messages in the given chat ID using the authority of the given bot. 

### Issue a 'killer poke' to a Telegram phishing bot

- TBC

