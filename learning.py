class learning:
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

  def printlist(self, word = ""):
    strtmp = ""
    for ws in self.words:
      if ws.word == word or word == "":
        strtmp += "[" + ws.word + ", " + ws.printlist() + "], "
    return strtmp

  def calculate_weight(self):
    for ws in self.words:
      ws.calculate_weight()

  def contains(self,word):
    for ws in self.words:
      if ws.word == word:
        return True
    return False

class wordStat: 
  def __init__(self, word): 
    self.word = word
    self.emojis = []    # creates a new empty list for each instances
  
  def add_emoji(self, emoji):
    self.emojis.append(emoji)
    
  def get_emoji(self,value):
    for e in self.emojis:
      if e.emoji == value:
        return e

  def get_top_emoji(self):
    self.emojis.sort(key=lambda emojiStat: emojiStat.reaction_weight, reverse=True)
    for e in self.emojis:
      if e.reaction_weight >= 0.5 or e.isConfirmed:
        return e

  def contains(self,emoji):
    for e in self.emojis:
      if e.emoji == emoji:
        return True
    return False

  def calculate_weight(self):
    for e in self.emojis:
      e.reaction_weight = e.reaction_count / e.word_count

  def printlist(self):
    strtmp = ""
    for e in self.emojis:
      strtmp += "[ " + str(e.emoji) + ", word_count: " + str(e.word_count) + ", reaction_count: " + str(e.reaction_count) + ", reaction_weight: " + str(e.reaction_weight) + ", isConfirmed: " + str(e.isConfirmed) + " ], "
    return strtmp

class emojiStat:
  def __init__(self, emoji, word_count, reaction_count): 
    # keep the emoji icon
    self.emoji = emoji
    # keep the origin word population 
    self.word_count = word_count
    # keep the reaction count
    self.reaction_count = reaction_count
    # keep the weight base on formula
    # reaction_count / word_count
    self.reaction_weight = reaction_count / word_count
    # identify if the emoji is confirmed as right one for the wordStat
    self.isConfirmed = False

