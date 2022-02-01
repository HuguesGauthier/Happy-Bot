from discord.ext import commands, tasks
import os
import asyncio
import discord
from replit import db
from keep_alive import keep_alive
import random
import jsonpickle
from learning import learning, wordStat, emojiStat

bot = commands.Bot(command_prefix='!')

@tasks.loop(minutes=30)
async def timer(bot):
	#for each server the bot own
	for server in bot.guilds:
		for channel in server.voice_channels:
			if len(channel.members) > 0:
				#play ramdomly song
				if len(db[server.name]) > 0:
					await playSong(server.name, channel,
														random.choice(db[server.name]))

############################
#event section
############################
@bot.event
async def on_ready():
	print('Logged in as {0.user}'.format(bot))

	timer.start(bot)

	global learned
	learned = jsonpickle.decode(db["Learned"])

	print(learned.printlist())


@bot.event
async def on_reaction_add(reaction, user):
	if reaction.message.author.bot:
		return
	if user == bot.user:
		return

	msg = reaction.message.content.lower()
	words = msg.split()

	for word in words:
		await addword(word, len(words), reaction)


@bot.event
async def on_message(message):
	if message.author.bot:
		return

	msg = message.content.lower()
	if msg[0:1] != "!":
		for word in msg.split():
			if learned.contains(word):
				#update word hits
				ws = learned.get_word(word)
				ws.word_hits += 1

				#add reaction on message
				emojis = ws.get_top_emoji()
				for e in emojis:
					try:
						await message.add_reaction(e.emoji)
					except:
						print("There is an emoji that this bot don't have access")

	learned.calculate_weight()

	await bot.process_commands(message)

	learned.calculate_weight()
	db["Learned"] = jsonpickle.encode(learned)


#########################
#command section
########################
@bot.command()
async def list(context):
	message = learned.printlist()
	info = (message[:3995] + '..') if len(message) > 3995 else message
	if message != "":
		await context.author.send(info)
	else:
		await context.author.send("list is empty")

@bot.command()
async def listword(context):
	msg = context.message.content
	if len(msg.split()) > 1:
		word = msg.split()[1]  #word
		message = learned.printlist(word)
		if message != "":
			await context.author.send(message)

@bot.command()
async def dellistword(context):
	msg = context.message.content
	if len(msg.split()) > 1:
		word = msg.split()[1]  #word
		learned.delete_word(word)
		await context.author.send(word + " deleted !")

@bot.command()
async def clearlist(context):
	learned.clear_word()
	await context.author.send("list cleared !")

########################
# function section
########################

async def playSong(servername, voice_channel, song):
	if voice_channel != None:
		print("Server: " + servername)
		print("Channel: " + voice_channel.name)
		print("Song: " + song)
		print("Listeners: ")
		for member in voice_channel.members:
			print(member)

		vc_connected = await voice_channel.connect()
		print(vc_connected)
		vc_connected.play(discord.FFmpegPCMAudio(song),
											after=lambda e: print('done', e))
		vc_connected.source = discord.PCMVolumeTransformer(vc_connected.source)
		vc_connected.source.volume = 1
		await asyncio.sleep(2.5)
		while vc_connected.is_playing():
			await asyncio.sleep(1.5)

		await vc_connected.disconnect()


async def addword(word, word_count, reaction):
	if not learned.contains(word):
		e = emojiStat(reaction.emoji, word_count, reaction.count)
		w = wordStat(word, 1)
		w.add_emoji(e)
		learned.add_word(w)
	else:
		ws = learned.get_word(word)
		if not ws.contains(reaction.emoji):
			e = emojiStat(reaction.emoji, word_count, reaction.count)
			ws.add_emoji(e)
		else:
			e = ws.get_emoji(reaction.emoji)
			e.word_count += word_count
			e.reaction_count += reaction.count

	if word_count == 1:
		e.isConfirmed = True


def initSong():
	ServerName = "HuguesDiscord"
	if ServerName in db.keys():
			del db[ServerName]

	db[ServerName] = []
	songList = db[ServerName]
	songList.append("./songs/haha.mp3")
	songList.append("./songs/happy.mp3")
	songList.append("./songs/behappy.mp3")
	songList.append("./songs/freeguy.mp3")
	songList.append("./songs/friday.mp3")
	songList.append("./songs/cantstopthefeeling.mp3")
	db[ServerName] = songList

	ServerName = "Happy Buds"
	if ServerName in db.keys():
			del db[ServerName]

	db[ServerName] = []
	songList = db[ServerName]
	songList.append("./songs/haha.mp3")
	#songList.append("./happy.mp3")
	#songList.append("./behappy.mp3")
	#songList.append("./freeguy.mp3")
	#songList.append("./friday.mp3")
	#songList.append("./cantstopthefeeling.mp3")
	db[ServerName] = songList

	ServerName = "Transit"
	if ServerName in db.keys():
			del db[ServerName]

	db[ServerName] = []
	# songList = db[ServerName]
	# songList.append("./happy.mp3")
	# songList.append("./behappy.mp3")
	# songList.append("./freeguy.mp3")
	# songList.append("./friday.mp3")
	# songList.append("./cantstopthefeeling.mp3")
	# db[ServerName] = songList


def initLearning():
	key = "Learned"
	#del db[key]
	if key not in db.keys():
			obj = learning()
			serialized = jsonpickle.encode(obj)
			db[key] = serialized
	# else:
	#     learned = jsonpickle.decode(db[key])
	#     print(learned.printlist())

	#     # for key in db:
	#     #   if key != "Learned":
	#     #     del db[key]


keep_alive()
initSong()
initLearning()

bot.run(os.getenv('token'))
