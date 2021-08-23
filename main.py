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
		pList = getPriceList()
		if len(pList) > 0:
			ores = "\n".join(list(map(lambda x: x[0], pList)))
			prices = "\n".join(list(map(lambda x: x[1], pList)))
			available = "\n".join(list(map(lambda x: x[2], pList)))
			embed=discord.Embed(title="Current Starbase Auction Prices", color=0xff2626)
			embed.add_field(name="Ore", value=ores, inline=True)
			embed.add_field(name="Price", value=prices, inline=True)
			embed.add_field(name="Available", value=available, inline=True)
			embed.set_footer(text="From starbase.auction/livefeed.txt")
			await message.channel.send(embed=embed)
		else:
			message.channel.send("No prices found :(")

client.run(os.getenv('DISCORD_TOKEN'))