import discord
import asyncio
from discord.voice_client import VoiceClient
from discord.ext.commands import Bot
from discord.ext import commands
import keys
bot  = commands.Bot('!')
vc_clients = {}


@bot.event
async def on_ready():
    global queue, playing_song
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    queue = []
    playing_song = False

@bot.command(pass_context = True)
async def play(ctx, filename):
	global queue
	global playing_song
	message = ctx.message
	
	queue.append(filename)
	print('add to queue')
       
	if ctx.message.server.id not in vc_clients:
		try:
			vc = await bot.join_voice_channel(message.author.voice_channel)
			vc_clients[message.server.id] = [vc]

		except Exception as e:
			print(e)
			return await bot.say("You are not in any voice channel.")

	def after():
		coro = stop_event.set()
		fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
		try:
			fut.result()
		except:
			pass

	try:
		while len(queue) > 0:
			if (playing_song == False):
				player = vc_clients[ctx.message.server.id][0].create_ffmpeg_player(queue[0], after=after)
				playing_song = True
				player.start()
				playing_song = False
				del queue[0]
				print(len(queue))
			else:
				print(1)
				await asyncio.sleep(1)
				continue
	except Exception as e:
		return await bot.say("ERROR: `%s"%e)

bot.run(keys.BOT_TOKEN)
