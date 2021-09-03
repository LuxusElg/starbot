import urllib.request
import discord
import os
import csv
from io import StringIO

client = discord.Client()

def getPriceList():
	try:
		with urllib.request.urlopen('https://docs.google.com/spreadsheets/d/19Ce3veTJyVLm_qoAqV4QWIJNODuXwLbvv2GhGB37Nkg/gviz/tq?tqx=out:csv&sheet=%20') as f:
			priceStr = f.read().decode('utf-8')
	except urllib.error.URLError as e:
		print(e.reason)
		return []
	f = StringIO(priceStr)
	reader = csv.reader(f, delimiter=',')
	formatted = list(row[0:4] for row in reader)
	orePrices = formatted[1:17]
	return orePrices

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
			embed=discord.Embed(title="Current Starbase Auction Prices", color=0xff2626)
			embed.add_field(name="Ore", value='\n'.join(ore[0] for ore in pList), inline=True)
			embed.add_field(name="Price", value='\n'.join(ore[1] for ore in pList), inline=True)
			embed.add_field(name="Available", value='\n'.join(ore[2] for ore in pList), inline=True)
			embed.add_field(name="% of NPC", value='\n'.join(ore[3] for ore in pList), inline=True)
			embed.set_footer(text="From Septic's Google Sheet")
			await message.channel.send(embed=embed)
		else:
			message.channel.send("No prices found :(")

client.run(os.getenv('DISCORD_TOKEN'))