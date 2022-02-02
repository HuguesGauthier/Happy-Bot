from discord.ext import commands, tasks
import os
import asyncio
import discord
from replit import db
from keep_alive import keep_alive
import random
import jsonpickle
from learning import learning, wordStat, emojiStat
from datetime import date

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
async def on_connect():
	await deserialize()

@bot.event
async def on_ready():
	print('Logged in as {0.user}'.format(bot))

	timer.start(bot)

	print(learned.printlist())

@bot.event
async def on_reaction_add(reaction, user):
	if reaction.message.author.bot:
		return
	if user == bot.user:
		return

	msg = reaction.message.content.lower()
	words = msg.split()
	word_count = len(words)

	# add every word
	for word in words:
		await addword(word, word_count, reaction)

	# add sentence
	await addword(msg, 1, reaction)

	await serialize()


@bot.event
async def on_message(message):
	if message.author.bot:
		return

	msg = message.content.lower()
	# dont check if its a command "!"
	if msg[0:1] != "!":
		for word in msg.split():
			if learned.contains(word):
				await addreaction(word,message)

		if learned.contains(msg) and len(msg.split()) > 1:
			await addreaction(word,message)

	learned.calculate_weight()

	await bot.process_commands(message)

	await serialize()

#########################
#command section
########################
@bot.command()
async def list(context):
	message = learned.printlist()
	info = (message[:2000] + '..') if len(message) > 2000 else message
	if message != "":
		await context.author.send(info)
	else:
		await context.author.send("list is empty")

@bot.command()
async def listword(context):
	msg = context.message.content
	if len(msg.split()) > 1:
		sentence= ""
		c = 0
		for word in msg.split():
			if c > 0:
				sentence += word + " "
			c +=1
		message = learned.printlist(sentence.strip())
		if message != "":
			await context.author.send(message)

@bot.command()
async def dellistword(context):
	msg = context.message.content
	if len(msg.split()) > 1:
		sentence= ""
		c = 0
		for word in msg.split():
			if c > 0:
				sentence += word + " "
			c +=1
		learned.delete_word(sentence.strip())
		await context.author.send(sentence + " deleted !")

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
			e.word_count_net += (word_count-1)
			e.reaction_count += reaction.count
			e.updatedon = date.today()

async def addreaction(word,message):
	#update word hits
	ws = learned.get_word(word)
	ws.word_hits += 1
	ws.updatedon = date.today()

	#add reaction on message
	emojis = ws.get_top_emoji()
	for e in emojis:
		try:
			await message.add_reaction(e.emoji)
		except:
			print("There is an emoji that this bot don't have access")

async def serialize():
	f = open("./learned/learned.txt", "w")
	f.write(jsonpickle.encode(learned))
	f.close()

async def deserialize():
	f = open("./learned/learned.txt")
	contents = f.read()
	f.close()
	global learned
	learned = jsonpickle.decode(contents)

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
	obj = learning()
	f = open("./learned/learned.txt", "w")
	f.write(jsonpickle.encode(obj))
	f.close()
	#key = "Learned"
	#del db[key]
	# if key not in db.keys():
	# 	obj = learning()
	# 	serialized = jsonpickle.encode(obj)
	# 	db[key] = serialized
	# else:
	#     learned = jsonpickle.decode(db[key])
	#     print(learned.printlist())

	#     # for key in db:
	#     #   if key != "Learned":
	#     #     del db[key]


keep_alive()
initSong()
#initLearning()

bot.run(os.getenv('token'))
