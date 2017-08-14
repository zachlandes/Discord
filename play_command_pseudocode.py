queue = []
playing_song = False

@bot.command(pass_context = True)
async def play(ctx, filename):
	queue.append(filename)

	def after():
		playing_song = False
		del queue[0]
	while len(queue) > 0:
		if playing_song = False:
			player = create_ffmpeg_player(queue[0], after=after)
			playing_song = True
			player.start()
		else:
			await asyncio.sleep(1)
			continue
