#!/usr/bin/python
from ai import *

class Player:
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
		total = self.subPlayer.initial_bet(self.__hand)
		if total < self.bank:
			self.amount = total
		elif self.bank > 5:
			self.amount = 10 * len(str(self.bank))
		else:
			self.amount = 5
		self.bank -= self.amount
		return self.amount

	def hit(self):
		return self.subPlayer.hit(self.subPlayer, self.__hand)

	def end_round(self, dealt):
		self.subPlayer.round_end(self.subPlayer, dealt)

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
	lst.append(Player('Patrick', HumanPlayer))
	lst.append(Player('Josh', Gambit))
	lst.append(Player('Mike', Gambit))
	lst.append(Player('Brennen', Brennen))
	lst.append(Player('Paul', all_in))
	lst.append(Player('Robert California', RobertCalifornia))
	lst.append(Player('Faggot Fish', faggotfish))
	lst.append(Player('Josh 2.0', Joshs_Pupil))
	return lst
