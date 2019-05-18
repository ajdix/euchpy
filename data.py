import numpy as np
import matplotlib.pyplot as plt

#!/usr/bin/env python
class data_card:
	# A class to represent a single card
	
	def __init__(self, newSuit, newValue):
		self.suit = newSuit #Suit
		self.value = newValue #Value, 9-A
		self.trump = False
		self.timesPlayed = 0.0
		self.timesWon = 0.0
		if (newSuit == 'diamonds' or newSuit == 'hearts'):
			self.color = 'red'
		else:
			self.color = 'black'
	
	def getWinPercentage(self):
		if self.timesPlayed >0:
			self.winPercentage = self.timesWon / self.timesPlayed
		else:
			self.winPercentage = 0

def parseData(images=False):
# Generate the deck of cards
	deck = []
	for suit in ['trump', 'notTrumpSameColor', 'notTrumpOffColor']:
		for value in [9., 10., 11., 12., 13., 14., 15., 16.]: #11=J, 12=Q, 13=K, 14=A
			deck.append(data_card(suit, value))

	tricks = 0
	winners = 0
	linesPerRound = 28
	resultDict = {'3-4': 0., 'all5': 0., 'euchre': 0.}
	totalResults = 0.

	with open("data_log.txt", "r") as f:
		
		for i, line in enumerate(f.readlines()):
			
			#print((i, line, i%linesPerRound, i%linesPerRound%5))
			
			if (i%linesPerRound == 0):
				trumpSuit = line.strip().split()[-1]
				
				if (trumpSuit == 'spades') or (trumpSuit == 'clubs'):
					trumpColor = 'black'
				else:
					trumpColor = 'red'
				
				if trumpSuit == 'spades':
					notTrumpSameColor = "clubs"
				elif trumpSuit == 'clubs':
					notTrumpSameColor = "spades"
				elif trumpSuit == 'hearts':
					notTrumpSameColor = "diamonds"
				elif trumpSuit == 'diamonds':
					notTrumpSameColor = "hearts"
					
				#print(trump, trumpColor, notTrumpSameColor)
				
			elif (i%linesPerRound == 1):
				tricks += 1
				pass
			
			elif (1 < i%linesPerRound < (linesPerRound-1)):
				suitPlayed = line.strip().split()[-1]
					
				if (suitPlayed == 'spades') or (suitPlayed == 'clubs'):
					colorPlayed = 'black'
				else:
					colorPlayed = 'red'
					
				valuePlayed = float(line.strip().split()[-3])
				
				#print(trumpSuit, colorPlayed, valuePlayed)
				
				if suitPlayed == trumpSuit:
					#print('here')
					for car in deck:
						if car.suit == 'trump':
							#print('here')
							if (abs(car.value - valuePlayed) < 0.01):
								#print('here')
								if (i%linesPerRound%5 != 1): 
									car.timesPlayed += 1.
								else:
									#print(line)
									#print("%f of %s won" %(car.value, car.suit))
									car.timesWon += 1.
									winners +=1
								break
				elif colorPlayed == trumpColor:
					for car in deck:
						if car.suit is 'notTrumpSameColor':
							if (abs(car.value - valuePlayed) < 0.01):
								if (i%linesPerRound != 6): 
									car.timesPlayed += 1.
								else:
									car.timesWon += 1.
									winners +=1
								break
				else:
					for car in deck:
						if car.suit == 'notTrumpOffColor':
							if (abs(car.value - valuePlayed) < 0.01):
								if (i%linesPerRound != 6): 
									car.timesPlayed += 1.
								else:
									car.timesWon += 1.
									winners +=1
								break
			elif i%linesPerRound == linesPerRound-1:
				result = line.strip().split()[0]
				
				resultDict[result] += 1
				totalResults += 1
					

	# Process data
	for car in deck: car.getWinPercentage()
	
	with open("card_values.txt", "w") as g:
		for car in deck:
			g.write("%s of %d - %f\n" %(car.suit, car.value, car.winPercentage))
	
	if images:
		# For Trump
		x = []
		y = []
		for car in deck:
			if car.suit == 'trump':
				x.append(car.value)
				y.append(car.winPercentage)
				#print(car.value, car.timesPlayed, car.timesWon, car.winPercentage)
				
		plt.bar(x, y, align='center', alpha=0.5)
		plt.xlabel('Card Value')
		plt.ylabel('Win Percentage')
		plt.title('Trump Card Win Percentage')
		plt.savefig('trump.png')
		plt.figure()
		# For notTrumpSameColor
		x = []
		y = []
		for car in deck:
			if car.suit == 'notTrumpSameColor':
				x.append(car.value)
				y.append(car.winPercentage)
				#print(car.value, car.timesPlayed, car.timesWon, car.winPercentage)
				
		plt.bar(x, y, align='center', alpha=0.5)
		plt.xlabel('Card Value')
		plt.ylabel('Win Percentage')
		plt.title('notTrumpSameColor Card Win Percentage')
		plt.savefig('notTrumpSameColor.png')
		plt.figure()
		# For notTrumpOffColor
		x = []
		y = []
		for car in deck:
			if car.suit == 'notTrumpOffColor':
				x.append(car.value)
				y.append(car.winPercentage)
				#print(car.value, car.timesPlayed, car.timesWon, car.winPercentage)
				
		plt.bar(x, y, align='center', alpha=0.5)
		plt.xlabel('Card Value')
		plt.ylabel('Win Percentage')
		plt.title('notTrumpOffColor Card Win Percentage')
		plt.savefig('notTrumpOffColor.png')
		plt.figure()

		# For result visualization
		x = [1, 3, 5]
		customXTicks = []
		y = []
		#print(resultDict)
		for result, frequency in resultDict.items():
			customXTicks.append(result)
			y.append(frequency / totalResults)

		plt.bar(x, y, align='center', alpha=0.5)
		plt.xticks(x, customXTicks)
		plt.ylabel('Frequency')
		plt.title('Result Frequency')
		plt.savefig('result_frequency.png')
		plt.figure()	

	print("%%%%%% Rounds analyzed: %d %%%%%%" %tricks)