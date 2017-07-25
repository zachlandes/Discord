import discord
import asyncio
from collections import defaultdict
import random
from discord.voice_client import VoiceClient
from discord.ext.commands import Bot
from discord.ext import commands
#TO DO: add function allowing command prefix to be set by user
bot  = commands.Bot('!')
vc_clients = {}






with open('keys', 'r') as f:
    keys = f.read().splitlines()

#import clips dictionary with {key:value} = {filename:[tags]}
#note that tags in clips file must be lowercase (change this )
file_path = 'audio_clips/'
clip_dict = {}
with open(file_path + 'clips', 'r') as f:
    for line in f:
        split_line = line.strip('\n').split('|')
        clip_dict[split_line[len(split_line)-1]] = split_line[:-1]

print(clip_dict)
@bot.event
async def on_ready():
    global playingsong, queue
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    playingsong = False
    queue = []

@bot.event
async def on_member_join(member):
    return await bot.send_message(member.server.default_channel, 'Welcome to {} !'.format(member.server.name))

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

                 
@bot.command(pass_context = True)
async def smak(ctx, *tags):
    global queue
    global playingsong
    message = ctx.message

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
                
    print(matches);

    if ctx.message.server.id in vc_clients:
        try:
            vc = await bot.join_voice_channel(message.author.voice_channel)
            vc_clients[message.server.id] = [vc]
        except Exception as e:
            print(e)
           
    if ctx.message.server.id not in vc_clients:
        try:
            vc = await bot.join_voice_channel(message.author.voice_channel)
            vc_clients[message.server.id] = [vc]
 
        except Exception as e:
            print(e)
            return await bot.say("You are not in any voice channel.")

    if not matches: #maybe add requestor name to error with message.author
            no_match_msg = discord.Embed(description =  "Damn - no matches! Try different tags", color = 0xff0000) #color must be hex, or discord.Color.?
            return await bot.say(embed=no_match_msg)
    else:
        max_val = max(matches.values())
        #print('max values: ' + str(max_val))
        max_files = [f for f, t in matches.items() if t == max_val]
        #print('max files: ' + str(max_files))
        file_choice = random.choice(max_files)
 
    try:


        mg = await bot.say("Loading...")
        print(1)
        player = vc_clients[ctx.message.server.id][0].create_ffmpeg_player(file_path+file_choice)
        if (player.is_playing() == False):
            playingsong = False
            print(2)
        if (playingsong == True):
            await bot.say("Added to queue")
            queue.append(file_path+file_choice)
            print(queue)
        else:
            vc_clients[message.server.id].append(player)
            player.start()
            playingsong = True
            """
            embed = discord.Embed(title = "Now playing :musical_note:", description = str(player.title), color = 0x0000FF)
            embed.add_field(name = "Duration (in seconds)", value = str(player.duration))
            embed.add_field(name = "Requested by", value = str(message.author))
            await bot.delete_message(mg)
            await bot.say(embed = embed)"""
            while True:
                if (playingsong == True):
                    continue
                else:
                    x = 1
                    player = vc_clients[ctx.message.server.id][0].create_ffmpeg_player(queue[x])
                    vc_clients[message.server.id].append(player)
                    player.start()
                    playingsong = True
                    """
                    embed = discord.Embed(title = "Now playing :musical_note:", description = str(player.title), color = 0x0000FF)
                    embed.add_field(name = "Duration (in seconds)", value = str(player.duration))
                    embed.add_field(name = "Requested by", value = str(message.author))
                    await bot.delete_message(mg)
                    await bot.say(embed = embed)"""
                    player.close_player(queue[x])
                    print(2312312)
                    x = x+1
                    await asyncio.sleep(1)
                    print(21312341252)
 
    except Exception as e:
        return await bot.say("ERROR: `%s"%e)

bot.run(keys[0])
