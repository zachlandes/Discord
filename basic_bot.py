import discord
import asyncio
from discord.ext import commands

bot  = commands.Bot('!')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_member_join(member):
    return await bot.send_message(member.server.default_channel, 'Welcome to {} !'.format(member.server.name))


"""
@bot.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await bot.send_message(message.channel, 'Calculating messages...')
        async for log in bot.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await bot.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await bot.send_message(message.channel, 'Done sleeping')
"""

@bot.command(pass_context = True)
async def ping(ctx):
    await bot.say("Pong!")

@bot.command(pass_context = True)
async def join(ctx):
    try:
        voice_channel = ctx.message.author.voice_channel
        await bot.join_voice_channel(voice_channel)
    except:
        my_embed = discord.Embed(description =  "Can't <join> - you're not in a voice channel!", color = 0xff0000) #color must be hex, or discord.Color.?
        return await bot.say(embed=my_embed)

@bot.command(pass_context = True)
async def leave(ctx):
    for c in bot.voice_clients:
        if(c.server == ctx.message.server):
            return await c.disconnect()

"""
embed = discord.Embed(title = "Some title", color = 0x00FF00) #color must be hex, or discord.Color.?
embed.add_field(name="A field", value="A value")
embed.add_field("Another field", "Another value for the field") #Can add more fields

return await client.say(embed = embed)
"""

#h/t Necro of Necrobot
@bot.command(pass_context = True)
async def play(ctx, filename):
    vc = ctx.message.author.voice_channel
    voice_client = await bot.join_voice_channel(vc)
    player = voice_client.create_ffmpeg_player(filename, after=lambda:close_player(filename))    
    #await bot.say(":musical_note: | Playing `" + player.title)

    player.start()


bot.run('MzI5NzY3ODQ1NzY2NjI3MzI4.DD7LKQ.7FoZd6R8CAOZdy8KKTMyS3EQB6g')
