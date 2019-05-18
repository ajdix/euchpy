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
		
		trumpValues = []
		with open("card_values.txt", "r") as wylie:
			for line in wylie.readlines():
				raw_line = line.strip().split()
				trumpValues.append(misc.card(raw_line[0], int(raw_line[2])))
				trumpValues[-1].winPercentage = float(raw_line[-1])
		
		#trumpValues = {9: 0.2, 10: 0.2, 12: 0.35, 13: 0.6, 14: 0.6, 11: 1.0}
		numSuit = 0
		suitsInHand = []
		if iter == 1:
			predictedTricksWon = 0
			for card in self.hand:
				if card.suit not in suitsInHand: suitsInHand.append(card.suit)
				if card.color == topOfKitty.color:
					if card.suit == topOfKitty.suit:
						numSuit += 1
						[thing for thing in trumpValues if (thing.suit == 'trump') and (thing.value == card.value)][0].winPercentage
					elif card.value == 11:
						
						predictedTricksWon += [thing for thing in trumpValues if (thing.suit == 'trump') and (thing.value == 15)][0].winPercentage
					else:
						predictedTricksWon += [thing for thing in trumpValues if (thing.suit == 'notTrumpSameColor') and (thing.value == card.value)][0].winPercentage
				else:
					predictedTricksWon += [thing for thing in trumpValues if (thing.suit == 'notTrumpOffColor') and (thing.value == card.value)][0].winPercentage
			
			# Count pick up
			if self.dealer:
				numSuit += 1
				predictedTricksWon += [thing for thing in trumpValues if (thing.suit == 'trump') and (thing.value == topOfKitty.value)][0].winPercentage
			
			# Adjust for a lot of trump
			if numSuit == 3: 
				predictedTricksWon += 0.5
			elif numSuit == 4:
				predictedTricksWon += 2.
				
			# Adjust for 2 suited
			if len(suitsInHand) <= 2:
				predictedTricksWon += 1.
			elif len(suitsInHand) == 4:
				predictedTricksWon += -0.5
			
			if predictedTricksWon >= 3.0:
				self.desiredTrump == topOfKitty.suit
				#print("Pick it up!")
				#if self.dealer: print("I'm the dealer, I get the %d of %s" %(topOfKitty.value, topOfKitty.suit))
				#for car in self.hand:
				#	print("%d of %s" %(car.value, car.suit))
				#print("Call %s, expect %f tricks" %(self.desiredTrump, predictedTricksWon))
				return True
			else:
				return False
		
		elif iter == 2:
			predictedTricksWon = {'spades': 0., 'clubs': 0., 'diamonds': 0., 'hearts': 0.}
			
			for card in self.hand:
				if card.suit not in suitsInHand: suitsInHand.append(card.suit)
			
			for dummy in [misc.card('spades', 0), misc.card('clubs', 0), misc.card('diamonds', 0), misc.card('hearts', 0)]:
				numSuit = 0
				for card in self.hand:
					if card.color == dummy.color:
						if card.suit == dummy.suit:
							predictedTricksWon[dummy.suit] += [thing for thing in trumpValues if (thing.suit == 'trump') and (thing.value == card.value)][0].winPercentage
							numSuit += 1
						elif card.value == 11:
							predictedTricksWon[dummy.suit] += [thing for thing in trumpValues if (thing.suit == 'trump') and (thing.value == 15)][0].winPercentage
							numSuit += 1
						elif card.value == 14:
							predictedTricksWon[dummy.suit] += [thing for thing in trumpValues if (thing.suit == 'notTrumpSameColor') and (thing.value == card.value)][0].winPercentage
					elif card.value == 14:
						predictedTricksWon[dummy.suit] += [thing for thing in trumpValues if (thing.suit == 'notTrumpOffColor') and (thing.value == card.value)][0].winPercentage
				
				# Adjust for lots of trump
				if numSuit == 3: 
					predictedTricksWon[dummy.suit] += 0.5
				elif numSuit == 4:
					predictedTricksWon[dummy.suit] += 2.
					
				# Adjust for two/four suited
				if len(suitsInHand) <= 2:
					predictedTricksWon[dummy.suit] += 1.
				elif len(suitsInHand) == 4:
					predictedTricksWon[dummy.suit] += -0.5
					
			
			expectedTricks = 0.0
			for suit, wins in predictedTricksWon.items():
				if suit != topOfKitty.suit:
					if wins > expectedTricks:
						expectedTricks = wins
						self.desiredTrump = suit
			
			if (expectedTricks >= 3.0) or self.dealer:
				#if self.dealer: 
					#print("Screwed!")
				#else:
				#	for car in self.hand:
				#		print("%d of %s" %(car.value, car.suit))
				#	print("Call %s, expect %f tricks" %(self.desiredTrump, expectedTricks))
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
			#print('%s is leading' %self.name)
			save = self.highestOffSuit()
			#print("Leading highest off suit: %d of %s" %(save.value, save.suit)) 
		
		try:
			save
		except NameError:
			print("Playing algorithm failed for %s" %self.name)
			save = self.lowestCard()
		
		self.hand.remove(save)
		return save
	