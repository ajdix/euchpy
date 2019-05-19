import random
from misc import *
class round:
	
	def __init__(self, playerList, kitten): #Initialize the round object
		self.players = playerList #List of players
		self.kitty = kitten #object to hold kitty cards, could be improved/removed
		self.teams = [team(playerList[0], playerList[2]), team(playerList[1], playerList[3])] # Simple team assignment
        				
		# Generate the deck of cards
		self.deck = []
		for suit in ['clubs', 'spades', 'hearts', 'diamonds']:
			for value in [9, 10, 11, 12, 13, 14]: #11=J, 12=Q, 13=K, 14=A
				self.deck.append(card(suit, value))
		
	def playGame(self):
		# Open the logs
		self.log = open("game_log.txt", "a")
		self.dataLog = open("data_log.txt", "a")
		self.teams[0].score = 0
		self.teams[1].score = 0
		while self.teams[0].score < 10 and self.teams[1].score < 10:
			self.playFullRound()
			
		self.log.write("Final Score:\n%s and %s: %d\n%s and %s: %d" %(self.teams[0].mem1.name, self.teams[0].mem2.name, self.teams[0].score, self.teams[1].mem1.name, self.teams[1].mem2.name, self.teams[1].score))
		self.log.close()
		self.dataLog.close()
		
	def playFullRound(self):
		# The basic structure of the game. Dealing, determining trump, play tricks, score, clean up.
		self.deal()		
		self.determineTrump()
		# Play 5 tricks
		self.playTrick()
		self.playTrick()
		self.playTrick()
		self.playTrick()
		self.playTrick()
		self.scoreRound()
		self.cleanUp()
		self.log.write("*" * 80)
		self.log.write("\n")
	
	def deal(self): # Function to deal cards to players
		random.seed()
		random.shuffle(self.deck)
		
		for i, person in enumerate(self.players):
			person.hand = self.deck[0 + 5*i:5 + 5*i] # Slice of the deck that is each persons hand
			self.kitty.cards = [self.deck[-1], self.deck[-2], self.deck[-3], self.deck[-4]] # Cards in the kitty
		
		# Print to game_log
		self.log.write("Kitty cards:\n")
		for card in self.kitty.cards:
			self.log.write("%s of %s\n" %(card.value, card.suit))
		self.log.write("\n")
		
		self.printHands()
		
		return
		
	def printHands(self): # function to print the hands of all the players. For convenience
		self.log.write("Printing players hands...\n")
		for player in self.players:
			self.log.write("%s:\n" %player.name)
			for card in player.hand:
				self.log.write("%d of %s\n" %(card.value, card.suit))
			self.log.write("\n")
			
	def determineTrump(self):
		trumpCalled = False
		kittySwitch = False
		self.log.write("Determining Trump: \n")
		self.log.write("Looking at %s\n" % self.kitty.getTop().suit)
		for i, player in enumerate(self.players):
			if player.lead:
				add = i # Save starting position index
				break
		
		playedCards = []
		for i in range(add, add+4):
			player = self.players[i % 4] # Determine active player
			
			if player.callTrump(self.kitty.getTop(), 1): # Call callTrump function with iter=1. If true, that's the trump
				self.trump = player.desiredTrump
				#print('Kittyyyyy')
				kittySwitch = True
				trumpCalled = True
				player.called = True
				self.teams[i%2].called = True
				self.log.write("We're playing %s\n -%s\n" %(self.trump, player.name))
				self.dataLog.write("We're playing %s\n -%s\n" %(self.trump, player.name))
				break # Once trump is decided, don't need to loop through the rest of the players
			else:
				# For the log
				self.log.write("Pass\n -%s\n" % player.name)
		
		if not trumpCalled: # Everbody passed
			for i in range(add, add+4):
				player = self.players[i % 4]
				
				if player.callTrump(self.kitty.getTop(), 2): # Call callTrump with iter=2. Will screw the dealer
					self.trump = player.desiredTrump
					trumpCalled = True
					player.called = True
					self.teams[i%2].called = True
					if player.dealer:
						self.log.write("%s was screwed\n" %player.name)
					self.log.write("We're playing %s\n -%s\n" %(self.trump, player.name))
					self.dataLog.write("We're playing %s\n -%s\n" %(self.trump, player.name))
					break # Again, don't call trump more than once
				else:
					self.log.write("Pass\n -%s\n" % player.name)
		
		if not trumpCalled:
			self.log.write("Error in the trump calling process") # This never triggers, but just in case
		
		for team in self.teams: # Could be rewritten in one line with list comprehension, maybe TODO
			if team.called:
				self.log.write("Team of %s and %s called it\n" %(team.mem1.name, team.mem2.name))
				break
		
		# do the kitty switching thing
		if kittySwitch:
			for player in self.players: 
				if player.dealer:
					player.hand.remove(player.lowestCard())
					player.hand.append(self.kitty.getTop())
					self.log.write("Modified hand\n")
					for car in player.hand:
						self.log.write("%d of %s\n" %(car.value, car.suit))
					self.log.write("\n")
					break # Save a few seconds
		
		# Fix the bauers, trump
		for player in self.players:
			for card in player.hand:
				if card.suit == self.trump: # This could be rewritten with looking at the color, but probably not that much better
					card.trump = True
					if card.value == 11:
						card.value = 16
				if card.value == 11:
					if (((self.trump == 'diamonds') or (self.trump == 'hearts')) and card.color == 'red'):
						card.value = 15
						card.trump = True
						card.suit = self.trump
					elif (((self.trump == 'clubs') or (self.trump == 'spades')) and card.color == 'black'):
						card.value = 15
						card.trump = True
						card.suit = self.trump
		
	
	def playTrick(self):
		# Figure out the lead
		for i, player in enumerate(self.players):
			if player.lead:
				add = i
				player.lead = False
				break
		
		# This is the part that plays the cards
		playedCards = []
		for i in range(add, add+4):
			activePlayer = self.players[i % 4]
			nextCard = activePlayer.playCard(playedCards, self.trump)
			self.log.write("%s plays the %d of %s\n" %(activePlayer.name, nextCard.value, nextCard.suit))
			self.dataLog.write("%s plays the %d of %s\n" %(activePlayer.name, nextCard.value, nextCard.suit))
			playedCards.append(nextCard)
		
		# Figure out which card won
		winner = findHighest(playedCards)
		winningPlayer = self.players[(add + playedCards.index(winner)) % 4]
		winningPlayer.tricksWon += 1
		winningPlayer.lead = True
		
		# Write info to game log and data log
		self.log.write("Winner: %d of %s\n" %(winner.value, winner.suit))
		self.dataLog.write("Winner: %d of %s\n" %(winner.value, winner.suit))
		
		self.log.write('%s wins\n' %self.players[(add + playedCards.index(winner)) % 4].name)
		self.log.write("-" * 80)
		self.log.write("\n")
		
	def scoreRound(self): # Function to determine who gets the points
		self.log.write("Scoring Round...\n")
		
		for team in self.teams:
			if team.called:
				self.log.write("Remember, %s and %s called it\n" %(team.mem1.name, team.mem2.name))
		
		# Loop through all the players, add the tricks won to their respective team's score
		for i, player in enumerate(self.players):
			for team in self.teams:
				if player is team.mem1 or player is team.mem2:
					team.tricks += player.tricksWon
			self.log.write("%s won %d tricks\n" %(player.name, player.tricksWon))
			self.log.write("So far, total of %d tricks for %s and %s\n" %(self.teams[i%2].tricks, self.teams[i%2].mem1.name, self.teams[i%2].mem2.name))
		# Total the tricks won, assign points	
		for team in self.teams:
			if team.called:
				if team.tricks >= 3 and team.tricks < 5:
					team.score += 1
					self.log.write("%s and %s got at least 3. 1 point" %(team.mem1.name, team.mem2.name))
					self.dataLog.write("3-4\n")
				elif team.tricks == 5:
					team.score += 2
					self.log.write("%s and %s won all 5! 2 points" %(team.mem1.name, team.mem2.name))
					self.dataLog.write("all5\n")
			else: # Euchre? I hardly knew er!
				if team.tricks >= 3:
					team.score += 2
					self.log.write("%s and %s got the euchre! 2 points" %(team.mem1.name, team.mem2.name))
					self.dataLog.write("euchre\n")
		self.log.write("\n")
		self.log.write("-" * 80)
		self.log.write("\n")
	def cleanUp(self): # Function to reset all the stuff that we've been messing with
		
		for team in self.teams:
			team.tricks = 0
			team.called = False
		
		for player in self.players:
			player.tricksWon = 0
			self.hand = []
			self.lead = False
			self.dealer = False
			self.called = False
			self.desiredTrump = 'squares' # Nonsense suit
			self.tricksWon = 0
		
		self.deck = []
		for suit in ['clubs', 'spades', 'hearts', 'diamonds']:
			for value in [9, 10, 11, 12, 13, 14]: #11=J, 12=Q, 13=K, 14=A
				self.deck.append(card(suit, value))
