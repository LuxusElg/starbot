import urllib.request
import discord
import os
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()

def getPriceList():
	try:
		with urllib.request.urlopen('https://starbase.auction/livefeed.txt') as f:
			priceStr = f.read().decode('utf-8')
	except urllib.error.URLError as e:
		print(e.reason)
		return []
	return list(map(lambda x: [x.split(":")[0].strip(), x.split(":")[1].split("-")[0].strip(), x.split(":")[1].split("-")[1].strip()], priceStr.split("|")))

@client.event
async def on_ready():
	print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	if message.content.startswith('!sbprices'):
		await message.channel.send('Prices!')

client.run(os.getenv('DISCORD_TOKEN'))