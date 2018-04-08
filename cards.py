#!/usr/bin/python
import random

class Card(object):
	rank = 1
	suit = 'S'
	"""docstring for Card"""
	def __init__(self, newRank, newSuit):
		self.rank = newRank
		self.suit = newSuit

	def __str__(self):
		return str(self.rank) + ' ' + self.suit

	def __add__(self, other):
		return self.rank + other.rank

	def __radd__(self, other):
		return self.rank + other

	def __str__(self):
		s = ''
		if self.suit == 'S':
			s = ' of Spades'
		elif self.suit == 'H':
			s = ' of Hearts'
		elif self.suit == 'C':
			s = ' of Clubs'
		else:
			s = ' of Diamonds'
		r = 0
		if self.rank == 1:
			r = 'Ace'
		elif self.rank == 11:
			r = 'Jack'
		elif self.rank == 12:
			r = 'Queen'
		elif self.rank == 13:
			r = 'King'
		else:
			r = self.rank
		return str(r) + s


class Deck(object):
	factor = 1
	decks = []

	"""docstring for Deck"""
	def __init__(self, totalDecks = 1):
		self.factor = totalDecks
		self.fill()
		self.shuffle()

	def fill(self):
		for _ in range(self.factor):
			for r in range(1, 14):
				for s in ['S', 'H', 'C', 'D']:
					self.decks.append(Card(r, s))

	def shuffle(self):
		random.shuffle(self.decks)

	def draw(self):
		if len(self.decks) == 0:
			self.fill()
			self.shuffle()
		return self.decks.pop()

	# def __str__(self):
	# 	return self.decks

if __name__ == '__main__':
	c1 = Card(5, 'S')
	c2 = Card(8, 'D')
	print(c1+c2)
	d = Deck()
	c = []
	for x in range(10):
		c.append(d.draw())

	print(sum(c))

	print(d.draw())
