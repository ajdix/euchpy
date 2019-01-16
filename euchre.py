import random
from collections import Counter
from itertools import cycle
from round import *
from player import *
from misc import *

################################################################################

liz = player('Liz')
bingley = player('Bingley')
darcy = player('Darcy')
jane = player('Jane')

players = [liz, bingley, darcy, jane]


kitten = kitty()

liz.lead = True
jane.dealer = True


game = round(players, kitten)

game.playGame()