class wordStat: 
  def __init__(self, word, count): 
    self.word = word
    self.count = count
    self.emojis = []    # creates a new empty list for each instances
  

  def add_emoji(self, emoji):
        self.emojis.append(emoji)


class emojiStat:
  def __init__(self, emoji, count ): 
    self.emoji = emoji 
    self.count = count