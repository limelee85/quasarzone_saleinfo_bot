import discord
from discord.ext.commands import Bot
import os

## init ##
TOKEN = os.getenv('TOKEN')
bot = discord.Client(intents=discord.Intents.default())

def sendMessage(text):

	embed = discord.Embed(title=text[0], colour = discord.Colour.blue())
	for item in text[1]:
		embed.add_field(name=item[0], value=item[1], inline=False) 

	@bot.event
	async def on_ready():
		for guild in bot.guilds:
			for channels in guild.text_channels:
				try :
					if (channels.topic.find('run_quasarzonebot') != -1) :
						print('[+] Send Message to {} - {}'.format(guild.name,channels.name))
						channel = bot.get_channel(int(channels.id))
						await channel.send(embed=embed) 
				except:
					continue
		await bot.close()

	bot.run(TOKEN)
