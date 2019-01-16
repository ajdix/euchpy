from collections import Counter
import misc
class player:
	# A class for the players
	
	def __init__(self, name):
		self.name = name
		self.hand = []
		self.lead = False
		self.dealer = False
		self.called = False
		self.desiredTrump = 'squares'
		self.tricksWon = 0
	
	def callTrump(self, topOfKitty, iter):
		suits = []
		for card in self.hand:
			suits.append(card.suit)
		sortedSuits = Counter(suits).most_common()
		
		#print(self.name)
		#print(sortedSuits)
		#print("\n")
		
		if sortedSuits[0][1] > 2: #call Trump
			self.desiredTrump = sortedSuits[0][0]
			call = True
		else:
			self.desiredTrump = sortedSuits[0][0]
			call = False
		
		if self.desiredTrump == topOfKitty.suit and call:
			return True
		elif (iter == 2 and call is True):
			return True
		elif (iter ==2 and self.dealer):
			return True
		else:
			return False
			
	def lowestCard(self):
		lowest = self.hand[0]
		for card in self.hand:
			if card.value < lowest.value and not card.trump:
				lowest = card
		#print("Lowest card is %d of %s" %(lowest.value, lowest.suit)) 
		return lowest
    
	def highestOffSuit(self):
		highest = self.hand[0]
		for card in self.hand:
			if card.value > highest.value and not card.trump:
				highest = card
		return highest
	
	def highestCard(self):
		highestValue = self.hand[0].value
		highest = self.hand[0]
		for i, card in enumerate(self.hand):
			if card.value > highestValue and card.trump:
				highestValue = card.value
				highest = card
				haveTrump = True
		if not haveTrump:
			highest = highestOffSuit
		return highest
	
	def playCard(self, cardsPlayed, trump):
		canFollow = False
		if cardsPlayed:
		
			playable = []
			
			for card in self.hand:
				if card.suit == cardsPlayed[0].suit:
					playable.append(card)
					canFollow = True
			
			if len(playable) == 0:
				for card in self.hand:
					if card.trump:
						playable.append(card)
				if not playable:
					playable.append(self.lowestCard())
			
			if len(playable) > 1:
			
				if canFollow:
					save = misc.findLowest(playable)
				else:
					trumper = misc.card(0, 'squares')
					for card in cardsPlayed:
						if card.trump and card.value > trumper.value:
							trumper = card
					
					for card in playable:
						if card.trump:
							if card.value > trumper.value:
								save = card
							else:
								save = self.lowestCard()
					
			else:
				save = playable[0]
		else:
			print('%s is leading' %self.name)
			save = self.highestOffSuit()
			print("Leading highest off suit: %d of %s" %(save.value, save.suit)) 
		
		try:
			save
		except NameError:
			print("Playing algorithm failed for %s" %self.name)
			save = self.lowestCard()
		
		self.hand.remove(save)
		return save
	