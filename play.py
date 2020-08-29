from marriage import *


# Now Players are collected form the file players.txt
L = []
with open('players.txt') as file:
	for line in file:
		L.append(line.strip())


P = [] # List of al the Players

for e in L:
	index = e.index(',')
	name = e[:index].strip()
	money = int(e[index+1:].strip())
	P.append(Player(name, money))


def play_game(n):
    '''n is the number of time marriage is Played.'''
    
    