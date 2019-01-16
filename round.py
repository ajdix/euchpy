import random
from misc import *
class round:
	
	def __init__(self, playerList, kitten):
		self.players = playerList
		self.kitty = kitten
		self.teams = [team(playerList[0], playerList[2]), team(playerList[1], playerList[3])]
		
		self.deck = []
		for suit in ['clubs', 'spades', 'hearts', 'diamonds']:
			for value in [9, 10, 11, 12, 13, 14]: #11=J, 12=Q, 13=K, 14=A
				self.deck.append(card(suit, value))
		for car in self.deck:
			print("%d of %s" %(car.value, car.suit))
		print("\n")

	def deal(self): # Function to deal cards to players
		random.seed()
		random.shuffle(self.deck)
		
		for i, person in enumerate(self.players):
			person.hand = self.deck[0 + 5*i:5 + 5*i]
			self.kitty.cards = [self.deck[-1], self.deck[-2], self.deck[-3], self.deck[-4]]
		
		print("Kitty cards: ")
		for card in self.kitty.cards:
			print("%s of %s" %(card.value, card.suit))
		print("\n")
		
		print("Player's Hands:")
		
		for player in self.players:
			print("%s:" %player.name)
			for card in player.hand:
				print("%d of %s" %(card.value, card.suit))
			print("\n")
		
		return
		
	def determineTrump(self):
		trumpCalled = False
		kittySwitch = False
		for i, player in enumerate(self.players):
			if player.callTrump(self.kitty.getTop(), 1):
				self.trump = player.desiredTrump
				
				kittySwitch = True
				trumpCalled = True
				player.called = True
				self.teams[i%2].called = True
		
		if not trumpCalled:
			for i, player in enumerate(self.players):
				if player.callTrump(self.kitty.getTop(), 2):
					self.trump = player.desiredTrump
					trumpCalled = True
					player.called = True
					self.teams[i%2].called = True
					break
		
		print("We're playing %s" %self.trump)
		for player in self.players:
			if player.called: print("-%s\n" %player.name)
			for card in player.hand:
				if card.suit == self.trump: 
					card.trump = True
					if card.value == 11:
						card.value = 16
				if card.value == 11:
					if ((self.trump == 'diamonds' or 'hearts') and card.color == 'red'):
						card.value = 15
						card.trump = True
						card.suit = self.trump
					elif ((self.trump == 'clubs' or 'spades') and card.color == 'black'):
						card.value = 15
						card.trump = True
						card.suit = self.trump
					else:
						raise('You fucked up')
		
		# do the kitty switching thing
		if kittySwitch:
			for player in self.players: 
				if player.dealer:
					player.hand.remove(player.lowestCard())
					player.hand.append(self.kitty.getTop())
					print("Modified hand")
					for car in player.hand:
						print("%d of %s" %(car.value, car.suit))
					print("\n")
	
	def playTrick(self):
		for i, player in enumerate(self.players):
			if player.lead:
				add = i
				player.lead = False
				break
		
		playedCards = []
		for i in range(add, add+4):
			activePlayer = self.players[i % 4]
			nextCard = activePlayer.playCard(playedCards, self.trump)
			print("%s plays the %d of %s\n" %(activePlayer.name, nextCard.value, nextCard.suit))
			playedCards.append(nextCard)
		
		winner = findHighest(playedCards)
		winningPlayer = self.players[(add + playedCards.index(winner)) % 4]
		winningPlayer.tricksWon += 1
		winningPlayer.lead = True
		
		
		print("%d of %s wins" %(winner.value, winner.suit))
		
		print('%s wins\n' %self.players[(add + playedCards.index(winner)) % 4].name)
		
	def scoreRound(self):
		
		for i, team in enumerate(self.players):
			self.teams[i%2].tricks += self.players[i].tricksWon
		
		for team in self.teams:
			#print(team.tricks)
			if team.called:
				if team.tricks > 3 and team.tricks < 5:
					team.score += 1
				elif team.tricks == 5:
					team.score += 2
			else:
				if team.tricks > 3:
					team.score += 2
		
	def cleanUp(self):
		
		for team in self.teams:
			team.tricks = 0
		
		for player in self.players:
			player.tricksWon = 0
			self.hand = []
			self.lead = False
			self.dealer = False
			self.called = False
			self.desiredTrump = 'squares'
			self.tricksWon = 0
			
		self.deck = []
		for suit in ['clubs', 'spades', 'hearts', 'diamonds']:
			for value in [9, 10, 11, 12, 13, 14]: #11=J, 12=Q, 13=K, 14=A
				self.deck.append(card(suit, value))
		for car in self.deck:
			print("%d of %s" %(car.value, car.suit))
		print("\n")


				
	def playFullRound(self):
		self.deal()		
		self.determineTrump()
		self.playTrick()
		self.playTrick()
		self.playTrick()
		self.playTrick()
		self.playTrick()
		self.scoreRound()
		self.cleanUp()
		
	def playGame(self):
		i=0
		while self.teams[0].score < 10 and self.teams[1].score < 10:
			self.playFullRound()
			
		print("Final Score:\n %s and %s: %d\n%s and %s: %d" %(self.teams[0].mem1.name, 
		self.teams[0].mem2.name, self.teams[0].score, self.teams[1].mem1.name, 
		self.teams[1].mem2.name, self.teams[1].score))