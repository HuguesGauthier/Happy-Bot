# Naive Bayes
# Naive Bayes algorithm works on Bayes theorem and takes a probabilistic approach, unlike other classification algorithms. The algorithm has a set of prior probabilities for each class. Once data is fed, the algorithm updates these probabilities to form something known as posterior probability. This comes useful when you need to predict whether the input belongs to a given list of classes or not.
from objprint import add_objprint

@add_objprint
class learning():
  
  def __init__(self): 
    self.words = []    # creates a new empty list for each instances

  def count(self):
    return len(self.words)

  def add_word(self,value):
    self.words.append(value)

  def get_word(self,value):
    for ws in self.words:
      if ws.word == value:
        return ws
        
  def clear_word(self):
    self.words.clear()

  def delete_word(self,value):
    index = -1
    c = 0
    for ws in self.words:
      if ws.word == value:
        index = c
        break
      c += 1
    if index != -1:
      self.words.pop(index)

  def calculate_stats(self):
    for ws in self.words:
      ws.calculate_stats()

  def contains(self,value):
    for ws in self.words:
      if ws.word == value:
        return True
    return False

  def get_top_hits(self, value):
    self.words.sort(key=lambda word: word.word_hits, reverse=True)
    for w in self.words:
      value -= 1
      if len(w.emojis) > 0 and value == 0:
        return w

@add_objprint
class word(): 

  def __init__(self, id, value, date):
    # message.id
    self.ids = [id]     
    # word of message.content
    self.word = value
    self.word_hits = 1
    self.emojis = []    # creates a new empty list for each instances
    self.createdon = date
    self.updatedon = None

  def update_word(self, id, date):
    if id not in self.ids:
      self.ids.append(id)
      self.word_hits += 1
      self.updatedon = date

  def add_emoji(self, emoji):
    self.emojis.append(emoji)
    
  def get_emoji(self,emoji):
    if type(emoji) is not str:
      # <:WhoMutedDJKhaled:756120713815130182>
      emoji = "<:" + emoji.name + ":" + str(emoji.id) + ">"
      
    for e in self.emojis:
      if e.emoji == emoji:
        return e

  def get_top_emoji(self):
    listtmp = []
    self.emojis.sort(key=lambda emoji: emoji.reaction_weight, reverse=True)
    for e in self.emojis:
      if (e.reaction_weight + e.reaction_appearance) / 2 >= 0.5 and self.word_hits >=3:
        listtmp.append(e)
    return listtmp

  def contains(self,emo):
    if type(emo) is not str:
      # <:WhoMutedDJKhaled:756120713815130182>
      emo = "<:" + emo.name + ":" + str(emo.id) + ">"
      
    for e in self.emojis:
      if e.emoji == emo:
        return True
    return False

  def calculate_stats(self):
    for e in self.emojis:
      e.reaction_appearance = e.reaction_count / self.word_hits
      e.reaction_weight = (e.reaction_count / e.word_count)

@add_objprint
class emoji():
  
  def __init__(self, emoji, word_count, reaction_count, date): 
    #print(type(emoji))
    # keep the emoji icon
    if type(emoji) is str:
      self.emoji = emoji
    else:
			# <:WhoMutedDJKhaled:756120713815130182>
      self.emoji = "<:" + emoji.name + ":" + str(emoji.id) + ">"
    # keep the sentence words count
    self.word_count = word_count
    # keep the sentence words count - 1
    self.word_count_net = word_count if word_count == 1 else word_count - 1
    # keep the reaction count
    self.reaction_count = reaction_count
    # keep the weight base on formula
    # (reaction_count / word_count) * self.reaction_appearance = 0
    self.reaction_weight = 0
    # keep the pourcentage of appearance
    # reaction_count / word_hits
    self.reaction_appearance = 0
    self.createdon = date
    self.updatedon = None