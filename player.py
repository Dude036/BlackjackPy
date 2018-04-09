#!/usr/bin/python
from ai import *

class Player(object):
	"""docstring for Player"""
	bank = 0
	amount = 0
	name = ''
	subPlayer = None
	__hand = None

	def __init__(self, newName, subPlayer):
		self.bank = 1000
		self.name = newName
		self.subPlayer = subPlayer

	def initial_bet(self):
		self.amount = self.subPlayer.initial_bet(self.__hand)
		self.bank -= self.amount
		return self.amount

	def hit(self):
		return self.subPlayer.hit(self.subPlayer, self.__hand)

	def won_money(self, percent):
		self.bank += (self.amount * percent) + self.amount

	def get_money(self):
		return self.bank

	def get_hand(self):
		return self.__hand

	def deal_hand(self, cards):
		self.__hand = cards

	def deal_card(self, card):
		self.__hand.append(card)
		if sum(self.__hand) > 21:
			return True
		else:
			return False


def getPlayers():
	lst = []
	lst.append(Player('Kevin', HumanPlayer))
	lst.append(Player('Alice', HumanPlayer))
	lst.append(Player('Josh', Gambit))

	return lst
