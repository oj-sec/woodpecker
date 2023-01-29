#!/usr/bin/env python3

# The Woodpecker is a Python utility for pulling data from Telegram phishing bots using Pyrogram. 

# Requires an API ID and API hash from a valid Telegram account associated with a telephone number. 
# Interacting with malicious accounts may get your Telegram account banned - use at your own risk. 

# pyrogram-2.0.97
# tgcrypto-1.2.5

from pyrogram import Client
import asyncio
import json
import requests
import argparse
import os

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Function to initialise a Telegram client for a given bot token
def initialise_bot(bot_token):
	config = read_config()
	api_id = config['telegramApiId']
	api_hash = config['telegramApiHash']
	output_config = ""
	if "output" in config.keys():
		output_config = config['output']
	bot = Client("bot", api_id, api_hash, bot_token=bot_token) 
	return bot, output_config

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

# Function to get the bot commands 
async def get_bot_commands(bot):

	async with bot:
		commands = await bot.get_bot_commands()
		return commands

# Function to issue a series of commands to purge the chat and cycle the bot token. 
#async def killer_poke(bot, chat_id=None):

# Async iterator for all messages the given chat
async def message_iterator(bot, chat_id, output, ticker=0):

	async with bot:

		ticker = 1
		flag = 0

		while True:
			iterator = []
			for i in range(0,200):
				iterator.append(ticker + i)
			messages = await bot.get_messages(chat_id, iterator)


			for message in messages:
				message = json.loads(str(message))
				if "empty" in message.keys():
					if message['empty'] == True:
						print("Encountered empty message.")
						flag = flag + 1
				else:
					writer(message, output)

			# Exit iterator if 200 empty messages in a row are encountered
			# Potentially naive break condition - needs testing
			if flag == 200:
				print("Breaking due to 200 concurrent empty messages.")
				break

			ticker = ticker + 200

	return 

# Function to handle result outputs
def writer(message, output):

	print(message)

	if output:
		if output['mode'] == "file":
			with open(output['destination'], "a") as f:
				f.write(message)
				f.write("\n")
		elif output['mode'] == "elastic":
			r = requests.post(output['destination'], headers={'Authorization': 'ApiKey ' + output['authorisation'], 'Content-Type': 'application/json'}, data=json.dumps(message), verify=False)
			print("\n")
			print(r.text)
			print("\n")

# Entrypoint & main execution handler
def main(bot_token, chat_id):

	try:
		os.remove("bot.session")
	except:
		pass

	bot, output_config = initialise_bot(bot_token)

	print("Client created sucessfuly using bot token & configuration.")
	loop = asyncio.get_event_loop()

	bot_info = loop.run_until_complete(get_user(bot))
	print("Bot information:")
	print(bot_info)

	chat = loop.run_until_complete(get_chat(bot, chat_id))

	if chat:
		print("Chat information:")
		print(chat)
		print("Iterating messages until empty:")

		all_messages = loop.run_until_complete(message_iterator(bot, chat_id, output_config))

	loop.close()

if __name__ == "__main__":

	parser = argparse.ArgumentParser(prog='Woodpecker',description="Telegram bot scraper & breaker.")
	parser.add_argument('--bot', '-b', required=True, help='Required - token for the target bot.')
	parser.add_argument('--chat', '-c', required=True, help='Required - chat ID for the tarket chat.')	

	args = parser.parse_args()

	main(args.bot, int(args.chat))