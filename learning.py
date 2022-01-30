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

  def printlist(self):
    strtmp = ""
    for ws in self.words:
      strtmp += "[" + ws.word + ", hits:" + str(ws.count) + ", " + ws.printlist() + "], "
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
  def __init__(self, word, count): 
    self.word = word
    self.count = count
    self.emojis = []    # creates a new empty list for each instances
  
  def add_emoji(self, emoji):
    self.emojis.append(emoji)
    
  def get_emoji(self,value):
    for e in self.emojis:
      if e.emoji == value:
        return e

  def contains(self,emoji):
    for e in self.emojis:
      if e.emoji == emoji:
        return True
    return False

  def calculate_weight(self):
    for e in self.emojis:
      e.weight = e.count * self.count

  def printlist(self):
    strtmp = ""
    for e in self.emojis:
      strtmp += "[" + e.emoji + ", hits:" + str(e.count) + ", weight:" + str(e.weight) + "], "
    return strtmp

class emojiStat:
  def __init__(self, emoji, count ): 
    self.emoji = emoji 
    self.count = count
    self.weight = 0