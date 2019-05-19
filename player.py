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
			
			if predictedTricksWon >= 2.0:
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
			
			if (expectedTricks >= 2.) or self.dealer:
				#if self.dealer: 
					#print("Screwed!")
				#else:
				#	for car in self.hand:
				#		print("%d of %s" %(car.value, car.suit))
				#	print("Call %s, expect %f tricks" %(self.desiredTrump, expectedTricks))
				return True
			else:
				return False
			
	def lowestCard(self, trump = 'squares'):
		lowest = self.hand[0]
		for card in self.hand:
			if card.value < lowest.value and not card.trump:
				lowest = card
			elif card.value == lowest.value:
				if card.color == misc.getColor(trump):
					lowest = card
					
			if lowest.trump: # If you have all trump, highest off suit is lowest trump
				if card.value < lowest.value:
					lowest = card
		#print("Lowest card is %d of %s" %(lowest.value, lowest.suit)) 
		return lowest
    
	def highestOffSuit(self, trump = 'squares'):
		highest = self.hand[0]
		for card in self.hand:
			if card.value > highest.value and not card.trump:
				highest = card
			elif card.value == highest.value:
				if card.color is not misc.getColor(trump):
					highest = card
		
			if highest.trump: # If you have all trump, highest off suit is lowest trump
				if card.value < highest.value:
					highest = card
			
		return highest
	
	def highestCard(self):
		highest = self.hand[0]
		for i, card in enumerate(self.hand):
			if card.value > highest.value and card.trump:
				highest = card
			elif card.value > highest.value and not highest.trump:
				highest = card
		return highest
	
	def playCard(self, cardsPlayed, trump):
		
		if len(cardsPlayed) == 0: # Determine if you're leading
			save = self.highestOffSuit(trump)
			if save.trump: # Don't lead the 9 of trump
				save = self.highestCard()
		else:
			ledSuit = cardsPlayed[0].suit
			onSuit = []
			for card in self.hand:
				if card.suit == ledSuit:
					onSuit.append(card)
			
			# Check if your partner is winning
			if len(cardsPlayed) > 2:
				if (cardsPlayed.index(misc.findHighest(cardsPlayed)) % 2 == (len(cardsPlayed) % 2)): # Partner is winning
					if len(onSuit) > 0:
						save = misc.findLowest(onSuit)
					else:	
						save = self.lowestCard(trump)
				else: # Partner is losing
					if len(onSuit) > 0:
						save = onSuit[0]
						for card in onSuit:
							if card.value > save.value:
								save = card
						if save.value < misc.findHighest(cardsPlayed).value:
							save = self.lowestCard(trump)
					else:
						save = self.highestCard()
						if not save.trump:
							save = self.lowestCard(trump)
			else: # Just win the trick if possible
				if len(onSuit) > 0:
					save = onSuit[0]
					for card in onSuit:
						if card.value > save.value:
							save = card
				else:
					save = self.highestCard()
					if not save.trump:
						save = self.lowestCard(trump)
		
		self.hand.remove(save)
		return save
	