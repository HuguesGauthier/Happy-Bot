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

@tasks.loop(minutes=10)
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

    print(learned.printlist())

@bot.event
async def on_connect():
    global learned 
    learned = jsonpickle.decode(db["Learned"])

@bot.event
async def on_disconnect():
    obj = jsonpickle.encode(learned)
    db["Learned"] = obj

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
    for word in msg.split():
        #print(word)
        if learned.contains(word):
            #update word hits
            ws = learned.get_word(word)
            ws.word_hits += 1

            #add reaction on message
            emojis = ws.get_top_emoji()
            for e in emojis:
              await message.add_reaction(e.emoji)

    learned.calculate_weight()

    await bot.process_commands(message)

    learned.calculate_weight()
    db["Learned"] = jsonpickle.encode(learned)


#########################
#command section
########################


@bot.command()
async def list(context):

    msg = context.message.content
    if len(msg.split()) > 1:
      word = msg.split()[1]  #word
      message = learned.printlist(word)
      if message != "":
        await context.author.send(learned.printlist(word))


@bot.command()
async def additem(context):
    msg = context.message.content
    listname = msg.split()[1]  #listname
    words = msg.split()  #words

    add_listitem(listname, words)

    message = listname + ": [" + ", ".join(db[listname]) + "]"
    await context.author.send(message)


@bot.command()
async def addlist(context):
    msg = context.message.content
    listname = msg.split()[1].replace("-", "")  #listname
    emoji = msg.split()[2]  #emoji
    add_reactList(listname, emoji)

    message = listname + ": [" + ", ".join(db[listname]) + "]"
    await context.author.send(message)


@bot.command()
async def dellist(context):
    msg = context.message.content
    listname = msg.split()[1]  #listname
    keys = db.keys()
    for key in keys:
        if key == listname:
            del db[key]


@bot.command()
async def delitem(context):
    msg = context.message.content
    listname = msg.split()[1]  #listname
    words = msg.split()  #words
    delete_listitem(listname, words)

    message = listname + ": [" + ", ".join(db[listname]) + "]"
    await context.author.send(message)


########################
# function section
########################
def add_listitem(listName, words):
    if listName in db.keys():
        reactList = db[listName]
        tmplist = []
        c = 0
        sentenceBool = False
        wordtmp = ""
        for word in words:
            if c > 1 and word not in reactList or sentenceBool:
                if word.find("]") >= 0:
                    wordtmp += word.replace("]", "")
                    tmplist.append(wordtmp)
                    sentenceBool = False
                    wordtmp = ""
                elif word.find("[") >= 0 or sentenceBool:
                    wordtmp += word.replace("[", "") + " "
                    sentenceBool = True
                else:
                    tmplist.append(word)
            c += 1

        reactList.extend(tmplist)
        db[listName] = reactList


def delete_listitem(listName, words):
    if listName in db.keys():
        reactList = db[listName]
        tmplist = []
        c = 0
        sentenceBool = False
        wordtmp = ""
        for word in words:
            if c > 1 or sentenceBool:
                if word.find("]") >= 0:
                    wordtmp += word.replace("]", "")
                    tmplist.append(wordtmp)
                    sentenceBool = False
                    wordtmp = ""
                elif word.find("[") >= 0 or sentenceBool:
                    wordtmp += word.replace("[", "") + " "
                    sentenceBool = True
                else:
                    tmplist.append(word)
            c += 1

        for item in tmplist:
            reactList.remove(item)

        db[listName] = reactList


def add_reactList(listName, emojiReturn):
    if listName not in db.keys():
        name = listName.replace("-", "")
        db[name] = []
        reactList = db[name]
        reactList.append(emojiReturn)
        db[name] = reactList


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
        w = wordStat(word,1)
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
