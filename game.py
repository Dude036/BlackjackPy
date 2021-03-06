#!/usr/bin/python

from cards import Deck
from player import Player, getPlayers
from ai import *
import sys


class Table(object):
	players = []
	dealerUp = []
	__dealerDownCard = None
	deck = Deck()
	verbose = False
	washed_up = []

	def __init__(self, loud=False):
		print("Welcome to BlackJack")
		self.verbose = loud

	def add_player(self, newPlayer):
		self.players.append(newPlayer)

	def setup_game(self):
		# Configure Deck for number of players
		self.deck = Deck(len(self.players)//2)

	def game(self):
		# Remove all broke players
		broke = []
		for you in self.players:
			if you.bank <= 0:
				broke.append(you)
		for them in broke:
			self.washed_up.append(self.players.pop(self.players.index(them)))
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
				print("\tRemaining Balance: $", you.bank)

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
		while sum(self.dealerUp) + self.__dealerDownCard < 15:
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
				you[2].won_money(1.5)
				winners.append(you)
			elif you[0] < 21 and you[0] >= dealerScore:
				# You still won, just less money
				you[2].won_money(1)
				winners.append(you)
			elif dealerScore > 21 and you[0] < 21:
				# Won
				you[2].won_money(1)
				winners.append(you)
			else:
				losers.append(you)

		# Print stuff
		if self.verbose:
			print("Winners!")

			print([you[:2] for you in winners])
			print("Losers")
			print([you[:2] for you in losers])

		# Remove cards from the Dealer
		self.dealerUp = []
		self.__dealerDownCard = None


if __name__ == '__main__':
	games_to_run = 100
	if len(sys.argv) > 1:
		try:
			games_to_run = eval(sys.argv[1])
		except Exception as e:
			pass

	starting_bank = 0

	t = Table()
	AIs = getPlayers()
	for you in AIs:
		t.add_player(you)
		starting_bank += you.bank

	t.setup_game()
	for _ in range(games_to_run):
		t.game()

	print("Winnings:")
	t.players.sort(reverse=True, key=lambda x: x.bank)
	format_str = '>' + str(max([len(n.name) for n in t.players]) + 1)

	for you in t.players:
		print(format(you.name, format_str), '$' + str(you.bank))

	net_bank = sum([1000 - you.bank for you in t.players]) + sum([1000 for i in range(len(t.washed_up))])
	print("Casino Final Net Balance $", net_bank)
	if net_bank > 0:
		print("Just goes to show, Gambling often leads to failure")
	else:
		print("Some of you got very lucky")
