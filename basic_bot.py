import discord
import asyncio
from discord.ext import commands
from collections import defaultdict
import random
import keys

#TO DO: add function allowing command prefix to be set by user
bot  = commands.Bot('!')


#import clips dictionary with {key:value} = {filename:[tags]}
#note that tags in clips file must be lowercase
file_path = 'audio_clips/'
clip_dict = {}
with open(file_path + 'clips', 'r') as f:
    for line in f:
        split_line = line.strip('\n').split('|')
        clip_dict[split_line[len(split_line)-1]] = split_line[:-1]

print(clip_dict)
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
    player = voice_client.create_ffmpeg_player(file_path + str(filename), after=lambda:close_player(file_path))    
    #await bot.say(":musical_note: | Playing `" + player.title)

    player.start()

#testing a function that will read user submitted tags
@bot.command(pass_context = True)
async def keyword(ctx, *tags):
    #TO DO: include code to handle case where no arg is passed
    user_tags = " ".join(tags).lower().split('|')
    
    print(user_tags)
    
    #create a dict of {filename:count of tag matches} for all files with at least 1 tag match
    matches = defaultdict(lambda: 0)
    for filename, tag_values in clip_dict.items():
        for value in tag_values:
            for tag in user_tags:
                if tag == value:
                    #print(filename)
                    matches[filename] +=1
                    #print(matches[filename]) 
                
    print(matches)

    #check if user in a voice channel, if so, check if bot is in the same channel
    vc = ctx.message.author.voice_channel
    if not vc:                              #if user is not in a voice channel tell them
        no_voice_msg = discord.Embed(description =  "Hey! You're not in a voice channel!", color = 0xff0000) #color must be hex, or discord.Color.?
        return await bot.say(embed=no_voice_msg)
    else:                                   #if user *is* in a voice channel
        for c in bot.voice_clients:
            if(c.server == ctx.message.server and c.channel == vc):   #if bot is in same voice channel as user break out of loop
                print(1)
                voice_client = c
                break
            elif(c.server == ctx.message.server):                     #if bot is in a different voice channel leave that channel and join author's
                print(2)
                await c.disconnect()
                voice_client = await bot.join_voice_channel(vc)
                break
        else:
            print(3)                                                         #if bot is not in a voice channel join the users voice channel
            voice_client = await bot.join_voice_channel(vc)
            
   
    #voice_client = await bot.join_voice_channel(vc)
    if not matches:
        no_match_msg = discord.Embed(description =  "Damn - no matches! Try different tags?", color = 0xff0000) #color must be hex, or discord.Color.?
        return await bot.say(embed=no_match_msg)
    else:
        max_val = max(matches.values())
        #print('max values: ' + str(max_val))
        max_files = [f for f, t in matches.items() if t == max_val]
        #print('max files: ' + str(max_files))
        file_choice = random.choice(max_files)
        player = voice_client.create_ffmpeg_player(file_path+file_choice, after=lambda:close_player(file_path+file_choice))

        player.start()
                    

bot.run(keys.BOT_TOKEN)
