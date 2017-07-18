import discord
import asyncio
from discord.ext import commands

client = discord.Client()

@client.event
async def on_message(message):
	#emoji = discord.utils.get(message.server.emojis, id='\U0001F44D')
	
	if message.author.id == '183038711972364288':
		await client.add_reaction(message, '\U0001F44D')


client.run('MzI5NzY3ODQ1NzY2NjI3MzI4.DD7LKQ.7FoZd6R8CAOZdy8KKTMyS3EQB6g')



"""
if "kappa" in message.content.lower():
        emoji = discord.utils.get(message.server.emojis, id='301806377414819841')
        await client.add_reaction(message, emoji)

"""