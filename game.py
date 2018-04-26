#!/usr/bin/python

from cards import Deck
from player import Player, getPlayers
from ai import *


class Table(object):
	players = []
	dealerUp = []
	__dealerDownCard = None
	deck = Deck()
	verbose = False

	"""docstring for Table"""
	def __init__(self, loud=False):
		print("Welcome to BlackJack")
		self.verbose = loud

	def add_player(self, newPlayer):
		self.players.append(newPlayer)

	def setup_game(self):
		# Configure Deck for number of players
		self.deck = Deck(len(self.players)//2)

	def game(self):
		# Deal all cards to players
		if self.verbose:
			print("Dealing Cards...")
		for x in self.players:
			x.deal_hand([self.deck.draw(), self.deck.draw()])
		# Dealer cards
		self.dealerUp.append(self.deck.draw())
		self.__dealerDownCard = self.deck.draw()
		if self.verbose:
			print("Dealer's upcard:\n\t" + str(self.dealerUp[0]))

		# Betting round
		self.betting_round()

		# Check who won and award money
		self.wrap_up(self.declare_winner())


	def declare_winner(self):
		winners = [(sum(self.dealerUp)+self.__dealerDownCard, 'Dealer', None)]
		if self.verbose:
			s = str(sum(self.dealerUp)+self.__dealerDownCard) + ' Dealer'
			print('Completed round scores:\n\t', s)
		for you in self.players:
			winners.append((sum(you.get_hand()), you.name, you))
			if self.verbose:
				s = str(sum(you.get_hand())) + ' ' + you.name
				print('\t', s)
		winners.sort()

		return winners


	def betting_round(self):
		in_round = []
		for you in self.players:
			in_round.append(you)
		# For all of the people in the game, get betting
		for you in self.players:
			bt = you.initial_bet()
			if self.verbose:
				print(you.name, "makes an initial bet of $"+str(bt))

		# While there are people still wanting to play, 
		while len(in_round) > 0:
			# Check all players for status
			for you in self.players:
				# Make sure they're still in
				if you not in in_round:
					pass
				# If they are playing, check if hit
				elif you.hit():
					# Deal card on hit
					bust = you.deal_card(self.deck.draw())
					if bust:
						in_round.remove(you)
				else:
					in_round.remove(you)

		# Dealers Turn once everyone has played
		while sum(self.dealerUp)+self.__dealerDownCard < 16:
			newCard = self.deck.draw()
			if self.verbose:
				print("Dealer draws a card.", newCard)
			self.dealerUp.append(newCard)

		if self.verbose:
			print("Dealer flips his card. It's a", self.__dealerDownCard)
			print("Dealers Hand:\n\t" + str(self.__dealerDownCard))
			for thing in self.dealerUp:
				print("\t" + str(thing))
		# Let all the players know what was played
		allhands = [self.__dealerDownCard]
		allhands.extend(self.dealerUp)
		for you in self.players:
			allhands.extend(you.get_hand())
		for you in self.players:
			you.end_round(allhands)


	def wrap_up(self, scores):
		# Complete the game an print all of the money won by player names.
		losers = []
		winners = []
		dealerScore = sum(self.dealerUp)+self.__dealerDownCard
		for you in scores:
			if you[2] is None:
				# Dealer, ignore his payday
				continue
			elif you[0] == 21:
				# Blackjack! Give them their money back and more
				you[2].won_money(2)
				winners.append(you)
			elif you[0] < 21 and you[0] >= dealerScore:
				# You still won, just less money
				you[2].won_money(1.5)
				winners.append(you)
			elif dealerScore > 21 and you[0] < 21:
				# Won
				you[2].won_money(1.5)
				winners.append(you)
			else:
				losers.append(you)

		# Print stuff
		if self.verbose:
			print("Winners!")
			print(winners)
			print("Losers")
			print(losers)

		# Remove cards from the Dealer
		self.dealerUp = []
		self.__dealerDownCard = None


if __name__ == '__main__':
	t = Table()
	AIs = getPlayers()
	for you in AIs:
		t.add_player(you)

	t.setup_game()
	for _ in range(1000000):
		t.game()

	print("Winnings:")
	t.players.sort(reverse=True, key=lambda x: x.bank)
	for you in t.players:
		print(you.name, you.bank - 1000)		
