from discord.ext import commands,tasks
import os
import asyncio
import discord
from replit import db
from keep_alive import keep_alive
import random
import jsonpickle
from learning import learning,wordStat,emojiStat

bot = commands.Bot(command_prefix = '!')

@tasks.loop(minutes=10)
async def timer(bot):

  #for each server the bot own
  for server in bot.guilds:
    for channel in server.voice_channels:
      if len(channel.members) > 0:
        #play ramdomly song
        await playSong(server.name, channel,random.choice(db[server.name]))


############################
#event section
############################   
@bot.event
async def on_ready():
  print('Logged in as {0.user}'
  .format(bot))

  timer.start(bot)

@bot.event
async def on_reaction_add(reaction, user):
  if user != bot.user:
    
    key = "Learned"
    learned = jsonpickle.decode(db[key])
      
    
    #if len(learning) == 0:
      #learning.append(["",0,[]])

    msg = reaction.message.content.lower()
    words = msg.split()
    for word in words:
      print(word)     
      if not learned.contains(word):
        e = emojiStat(reaction.emoji,reaction.count)
        w = wordStat(word,1)
        w.add_emoji(e)
        #print(w)
        learned.add_word(w)
      else:
        ws = learned.get_word(word)
        ws.count += 1
        if not ws.contains(reaction.emoji):
          e = emojiStat(reaction.emoji,reaction.count)
          ws.add_emoji(e)
        else:
          e = ws.get_emoji(reaction.emoji)
          e.count += reaction.count

        #await addWordStat(learning,word,1,reaction)
      # for sublist in learning[0][0]:
      #   print(sublist)
      #   if word not in sublist:
      #     reactionEmoji = [reaction.emoji,reaction.count]
      #     print(reactionEmoji)
      #     wordstat = [word,1,reactionEmoji]
      #     print(wordstat)
      #     learning.append(wordstat)
      #   else:
      #     wordstat = learning[word]
      #     print(wordstat)
    
    learned.calculate_weight()
    obj = jsonpickle.encode(learned)
    db[key] = obj

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  
  #search in ractions list
  msg = message.content.lower()
  for key in db:
    if key != "Learned":
      listtmp = db[key]
      for word in msg.split():
        if word in listtmp:
          await message.add_reaction(listtmp[0])

  #search the reaction list's phrase in the input msg
  for key in db:
    if key != "Learned": 
      listtmp = db[key]
      for word in listtmp:
        words = word.split()
        wordcount = len(words)
        if wordcount > 1:
          if msg.find(word) != -1:
            await message.add_reaction(listtmp[0])

  #search the input msg with emoji in list
  for key in db:
    if key != "Learned":
      listtmp = db[key]
      if msg.find(listtmp[0]) != -1:
        await message.add_reaction(listtmp[0])

  await bot.process_commands(message)

#########################
#command section
########################

@bot.command()
async def list(context):

  for key in db:
    if key != "Learning":
      print(key+": ["+ ", ".join(db[key])+"]")
  
  msg = context.message.content
  listname = msg.split()[1] #listname

  for key in db:
    if key == listname:
      message = key+": ["+ ", ".join(db[key])+"]"
      await context.author.send(message)

@bot.command()
async def additem(context):
  msg = context.message.content
  listname = msg.split()[1] #listname
  words = msg.split() #words
  
  add_listitem(listname,words)

  message = listname+": ["+ ", ".join(db[listname])+"]"
  await context.author.send(message)    

@bot.command()
async def addlist(context):
  msg = context.message.content
  listname = msg.split()[1].replace("-","") #listname
  emoji = msg.split()[2] #emoji
  add_reactList(listname,emoji)

  message = listname+": ["+ ", ".join(db[listname])+"]"
  await context.author.send(message)   

@bot.command()
async def dellist(context):
  msg = context.message.content
  listname = msg.split()[1] #listname
  keys = db.keys()
  for key in keys: 
    if key == listname:   
      del db[key]

@bot.command()
async def delitem(context):
  msg = context.message.content
  listname = msg.split()[1] #listname
  words = msg.split() #words
  delete_listitem(listname,words)
  
  message = listname+": ["+ ", ".join(db[listname])+"]"
  await context.author.send(message) 

######################## 
# function section   
########################  
def add_listitem(listName,words):
  if listName in db.keys():
    reactList = db[listName]
    tmplist = []
    c = 0
    sentenceBool = False
    wordtmp = ""
    for word in words:
      if c > 1 and word not in reactList or sentenceBool:
        if word.find("]") >= 0:
          wordtmp += word.replace("]","")
          tmplist.append(wordtmp)
          sentenceBool = False
          wordtmp = ""
        elif word.find("[") >= 0 or sentenceBool:
          wordtmp += word.replace("[","") + " "
          sentenceBool = True
        else:
          tmplist.append(word)
      c += 1

    reactList.extend(tmplist)
    db[listName] = reactList
  
def delete_listitem(listName,words):
  if listName in db.keys():
    reactList = db[listName]
    tmplist = [] 
    c = 0
    sentenceBool = False
    wordtmp = ""
    for word in words:
      if c > 1 or sentenceBool:
        if word.find("]") >= 0:
          wordtmp += word.replace("]","")
          tmplist.append(wordtmp)
          sentenceBool = False
          wordtmp = ""
        elif word.find("[") >= 0 or sentenceBool:
          wordtmp += word.replace("[","") + " "
          sentenceBool = True
        else:
          tmplist.append(word)
      c += 1

    for item in tmplist:
      reactList.remove(item)

    db[listName] = reactList

def add_reactList(listName, emojiReturn):
  if listName not in db.keys():
    name = listName.replace("-","")
    db[name] = []
    reactList = db[name]
    reactList.append(emojiReturn)
    db[name] = reactList

async def playSong(servername,voice_channel,song):
  if voice_channel != None:
    print("Server: " + servername)
    print("Channel: " + voice_channel.name)
    print("Song: " + song)
    print("Listeners: ")
    for member in voice_channel.members:
      print(member)

    vc_connected = await voice_channel.connect()
    print(vc_connected)
    vc_connected.play(discord.FFmpegPCMAudio(song), after=lambda e: print('done', e))    
    vc_connected.source = discord.PCMVolumeTransformer(vc_connected.source)
    vc_connected.source.volume = 1
    await asyncio.sleep(2.5)
    while vc_connected.is_playing():
      await asyncio.sleep(1.5)

    await vc_connected.disconnect()

async def addWordStat(learning,word,count,reaction):
  print(learning)
  print(word)
  print(count)
  print(reaction)
  e = emojiStat(reaction.emoji,reaction.count)
  print(e.emoji)
  print(e.count)
  w = wordStat(word,count)
  w.add_emoji(e)
  print(w.word)
  print(w.count)
  print(w.emojis)
  learning.append(w)
  #l = db["Learning"]
  #l.append(w)
  #db["Learning"] = l

def initSong():
  ServerName = "HuguesDiscord"
  if ServerName in db.keys():
    del db[ServerName]

  db[ServerName] = []
  songList = db[ServerName]
  songList.append("./haha.mp3")
  songList.append("./happy.mp3")
  songList.append("./behappy.mp3")
  songList.append("./freeguy.mp3")
  songList.append("./friday.mp3")
  songList.append("./cantstopthefeeling.mp3")
  db[ServerName] = songList

  ServerName = "Happy Buds"
  if ServerName in db.keys():
    del db[ServerName]
    
  db[ServerName] = []
  songList = db[ServerName]
  songList.append("./haha.mp3")
  songList.append("./happy.mp3")
  songList.append("./behappy.mp3")
  songList.append("./freeguy.mp3")
  songList.append("./friday.mp3")
  songList.append("./cantstopthefeeling.mp3")
  db[ServerName] = songList

  ServerName = "Transit"
  if ServerName in db.keys():
    del db[ServerName]
    
  db[ServerName] = []
  songList = db[ServerName]
  songList.append("./happy.mp3")
  songList.append("./behappy.mp3")
  songList.append("./freeguy.mp3")
  songList.append("./friday.mp3")
  songList.append("./cantstopthefeeling.mp3")
  db[ServerName] = songList

def initLearning():
  key = "Learned"
  #del db[key]
  if key not in db.keys():
    obj = learning()
    serialized = jsonpickle.encode(obj)
    db[key] = serialized
  else:
    learned = jsonpickle.decode(db[key])
    print(learned.printlist())

    # e = emojiStat("poop",1)
    # w = wordStat("caca",1)
    # w.add_emoji(e)
    # print(w)
    # learned.add(w)

    #print(learned)
    #serialized = jsonpickle.encode(learned)
    #db[key] = serialized

  #del db[key]

keep_alive()
initSong()
initLearning()

bot.run(os.getenv('token'))