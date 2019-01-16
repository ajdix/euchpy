class card:
	# A class to represent a single card
	
	def __init__(self, newSuit, newValue):
		self.suit = newSuit #Suit
		self.value = newValue #Value, 9-A
		self.trump = False
		if newValue == 11:
			if (newSuit == 'diamonds' or newSuit == 'hearts'):
				self.color = 'red'
			else:
				self.color = 'black'


class kitty:
	def __init__(self):
		self.cards = []
		
	def getTop(self):
		return self.cards[0]
		
class team:
	def __init__(self, mem1, mem2):
		self.score = 0
		self.called = False
		self.tricks = 0
		self.mem1 = mem1
		self.mem2 = mem2
		
def findLowest(cards):
	allTrump = False
	for card in cards:
		if not card.trump:
			lowest = card
			break
	try:
		highest
	except NameError:
		allTrump = True
		lowest = cards[0]

	if not allTrump:
		for card in cards:
			if (card.value < lowest.value and not card.trump):
				lowest = card
	else:
		for card in cards:
			if (card.value < lowest.value):
				lowest = card
	return lowest
	
def findHighest(cards):
	noTrump = False
	for card in cards:
		if card.trump:
			highest = card
			break
	try:
		highest
	except NameError:
		noTrump = True
		highest = cards[0]
	
	if noTrump:
		for card in cards:
			if (card.value > highest.value):
				highest = card
	else:
		for card in cards:
			if (card.value > highest.value and card.trump):
				highest = card
	return highest