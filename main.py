import urllib.request
import discord
import os
from bs4 import BeautifulSoup
#from dotenv import load_dotenv

#load_dotenv()
client = discord.Client()

def getPriceList():
	try:
		with urllib.request.urlopen('https://docs.google.com/spreadsheets/d/19Ce3veTJyVLm_qoAqV4QWIJNODuXwLbvv2GhGB37Nkg/edit#gid=1157372011') as f:
			priceStr = f.read().decode('utf-8')
	except urllib.error.URLError as e:
		print(e.reason)
		return []
	soup = BeautifulSoup(priceStr, "lxml")
	tables = soup.find_all("table")
	formatted = list(list(list(td.text for td in row.find_all("td")) for row in table.find_all("tr")) for table in tables)
	orePrices = formatted[0][3][33:48]
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
		oList = ['Kutonium', 'Arkanium', 'Valkite', 'Nhurgite', 'Karnite','Vokarium','Charodium','Ajatite','Bastium','Exorium','Aegisium','Ice','Ymrite','Surtrite','Corazium']
		if len(pList) > 0:
			ores = "\n".join(oList)
			prices = "\n".join(pList)
			embed=discord.Embed(title="Current Starbase Auction Prices", color=0xff2626)
			embed.add_field(name="Ore", value=ores, inline=True)
			embed.add_field(name="Price", value=prices, inline=True)
			embed.set_footer(text="From Septic's Google Sheet")
			await message.channel.send(embed=embed)
		else:
			message.channel.send("No prices found :(")

client.run(os.getenv('DISCORD_TOKEN'))