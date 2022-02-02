# Naive Bayes
# Naive Bayes algorithm works on Bayes theorem and takes a probabilistic approach, unlike other classification algorithms. The algorithm has a set of prior probabilities for each class. Once data is fed, the algorithm updates these probabilities to form something known as posterior probability. This comes useful when you need to predict whether the input belongs to a given list of classes or not.

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

	def printlist(self, word = ""):
		strtmp = ""
		for ws in self.words:
			if ws.word == word or word == "":
				strtmp += "\r\n\r\n[ word: " + ws.word + ", word_hits: " + str(ws.word_hits) + ", emojis: " + ws.printlist() + "], "
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
	def __init__(self, word, hits):
		self.word = word
		self.word_hits = hits
		self.emojis = []    # creates a new empty list for each instances
  
	def add_emoji(self, emoji):
		self.emojis.append(emoji)
    
	def get_emoji(self,value):
		for e in self.emojis:
			if e.emoji == value:
				return e

	def get_top_emoji(self):
		listtmp = []
		#self.emojis.sort(key=lambda emojiStat: emojiStat.isConfirmed, reverse=True)
		#for e in self.emojis:
		#	if e.isConfirmed:
		#		listtmp.append(e)
    
		if len(listtmp) == 0:
			self.emojis.sort(key=lambda emojiStat: emojiStat.reaction_weight, reverse=True)
			for e in self.emojis:
				if (e.reaction_weight + e.reaction_appearance) / 2 >= 0.5:
					listtmp.append(e)
		return listtmp

	def contains(self,emoji):
		for e in self.emojis:
			if e.emoji == emoji:
				return True
		return False

	def calculate_weight(self):
		for e in self.emojis:
			e.reaction_appearance = e.reaction_count / self.word_hits
			e.reaction_weight = (e.reaction_count / e.word_count )

			#if e.reaction_weight >= 1 and self.word_hits >=5:
			#	e.isConfirmed = True

	def printlist(self):
		strtmp = ""
		for e in self.emojis:
			strtmp += "[ " + str(e.emoji) + ", word_count: " + str(e.word_count) + ", reaction_count: " + str(e.reaction_count) + ", reaction_weight: " + str(e.reaction_weight) + ", reaction_appearance: " + str(e.reaction_appearance) +", isConfirmed: " + str(e.isConfirmed) + " ], "
		return strtmp

class emojiStat:
  def __init__(self, emoji, word_count, reaction_count): 

		# keep the emoji icon
    self.emoji = emoji
		# keep the sentence words count - 1
    self.word_count = word_count
		# keep the reaction count
    self.reaction_count = reaction_count
		# keep the weight base on formula
		# (reaction_count / word_count) * self.reaction_appearance = 0
    self.reaction_weight = 0
		# keep the pourcentage of appearance
		# reaction_count / word_hits
    self.reaction_appearance = 0
		# identify if the emoji is confirmed as right one for the wordStat
		# the word_hits must be at least at 5
    self.isConfirmed = False