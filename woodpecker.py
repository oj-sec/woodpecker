#!/usr/bin/env python3

# The Woodpecker is a Python utility for pulling data from Telegram phishing bots using Pyrogram. 

# Requires an API ID and API hash from a valid Telegram account associated with a telephone number. 
# Interacting with malicious accounts may get your Telegram account banned - use at your own risk. 

# pyrogram-2.0.97
# tgcrypto-1.2.5

from pyrogram import Client
import asyncio
import json

# Function to initialise a Telegram client for a given bot session
def initialise(bot_token):
	config = read_config()
	api_id = config['telegramApiId']
	api_hash = config['telegramApiHash']
	output = ""
	if "output" in config.keys():
		output = config['output']
	bot = Client("bot", api_id, api_hash, bot_token=bot_token) 
	return bot, output

# Function to read config.ini file.
def read_config():
	try:
		with open('config.ini', 'r') as c:
			config = json.loads(c.read())
			return config
	except FileNotFoundError:
		return

# Function to retrieve the metadata object for a given chat
async def get_chat(bot, chat_id):

	async with bot:
		chat = await bot.get_chat(chat_id)
		return chat

# Function to retrieve detailed information user by name or id
# Returns self by default
async def get_user(bot, username="me"):

	async with bot:
		user = await bot.get_users(username)
		return user

# Async iterator for all messages the given chat
async def message_iterator(bot, chat_id, output, ticker=0):

	async with bot:

		ticker = 1

		while True:
			iterator = []
			for i in range(0,200):
				iterator.append(ticker + i)
			messages = await bot.get_messages(chat_id, iterator)

			flag = False

			for message in messages:
				message = json.loads(str(message))
				if "empty" in message.keys():
					if message['empty'] == True:
						flag = flag + 1
						break
				else:
					print(message)
					writer(message)

			# Exit iterator if 200 empty messages in a row are encountered
			# Potentially naive break condition - needs testing
			if flag == 200:
				break

			ticker = ticker + 200

	return 

def writer(message):
	with open("test3", 'a') as f:
		json.dump(message, f)
		f.write("\n")

# Entrypoint & main execution handler
def main(bot_token, chat_id):

	bot, output = initialise(bot_token)
	loop = asyncio.get_event_loop()
	chat = loop.run_until_complete(get_chat(bot, chat_id))
	chat_member = loop.run_until_complete(get_user(bot, ""))
	chat_member = loop.run_until_complete(get_user(bot, "me"))

	print(chat_member)
	quit()

	if chat:

		all_messages = loop.run_until_complete(message_iterator(bot, chat_id, output))

