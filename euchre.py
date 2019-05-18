#!/usr/bin/env python
import random
from collections import Counter
from itertools import cycle
from round import *
from player import *
from misc import *
from data import *
import argparse

################################################################################
parser = argparse.ArgumentParser(description='Run some euchre games, process the data from them')
parser.add_argument('numGames', type=int, help='Number of games to run')
parser.add_argument('--data', action='store_true', help='Option to run data analysis routine')
parser.add_argument('--images', action='store_true', help='Option to make images')
parser.add_argument('--clear_logs', action='store_true', help='Option to clear logs')

args = parser.parse_args()

#print(args.numGames, args.data, args.images)

liz = player('Liz')
bingley = player('Bingley')
darcy = player('Darcy')
jane = player('Jane')

players = [liz, bingley, darcy, jane]


kitten = kitty()

liz.lead = True
jane.dealer = True


game = round(players, kitten)

if args.clear_logs:
	open('game_log.txt', 'w').close()
	open('data_log.txt', 'w').close()

for i in range(0, args.numGames):
	game.playGame()

if args.data:
	parseData(images=args.images)