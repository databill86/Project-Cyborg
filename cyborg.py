import sys

# Twitter Login
import twitter
from keys import keys

api = twitter.Api(consumer_key=keys[0][1],
    consumer_secret=keys[1][1],
    access_token_key=keys[2][1],
    access_token_secret=keys[3][1])

# Get tweets of a CLI arg username
s = api.GetUserTimeline(screen_name=sys.argv[1])
statuses = [each.text for each in s]
 
bin = ''
import unicodedata
for each in statuses:
    bin += unicodedata.normalize('NFKD', each).encode('ascii','ignore') + '\n'

# Markov Class object. shout out to @agiliq!!!!
import random
class Markov(object):

	def __init__(self, bin):
		self.cache = {}
		#self.open_file = open_file
		self.words = self.file_to_words()
		self.word_size = len(self.words)
		self.database()
		
	
	def file_to_words(self):
		#self.open_file.seek(0)
		data = bin
		words = data.split()
		return words
		
	
	def triples(self):
		
		if len(self.words) < 3:
			return
		
		for i in range(len(self.words) - 2):
			yield (self.words[i], self.words[i+1], self.words[i+2])
			
	def database(self):
		for w1, w2, w3 in self.triples():
			key = (w1, w2)
			if key in self.cache:
				self.cache[key].append(w3)
			else:
				self.cache[key] = [w3]
				
	def generate_markov_text(self, size=25):
		seed = random.randint(0, self.word_size-3)
		seed_word, next_word = self.words[seed], self.words[seed+1]
		w1, w2 = seed_word, next_word
		gen_words = []
		for i in xrange(size):
			gen_words.append(w1)
			w1, w2 = w2, random.choice(self.cache[(w1, w2)])
		gen_words.append(w2)
		return ' '.join(gen_words)
        
        
#f = open(sys.argv[1])
m = Markov(bin)
print m.generate_markov_text()
