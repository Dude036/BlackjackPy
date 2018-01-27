#!/usr/bin/python

from cards import Deck
from player import Player
from ai import *


class Table(object):
	players = []
	dealerUp = []
	__dealerDownCard = None
	deck = Deck()

	"""docstring for Table"""
	def __init__(self):
		print("Welcome to BlackJack")

	def add_player(self, newPlayer):
		self.players.append(newPlayer)

	def game(self):
		# Configure Deck for number of players
		self.deck = Deck(len(self.players)//2)
		# Deal all cards to players
		for x in self.players:
			x.deal_hand([self.deck.draw(), self.deck.draw()])
		# Dealer cards
		self.dealerUp.append(self.deck.draw())
		self.__dealerDownCard = self.deck.draw()

		# Betting round
		self.betting_round()

		# Check who won and award money
		self.wrap_up(self.declare_winner())


	def declare_winner(self):
		winners = [(sum(self.dealerUp)+self.__dealerDownCard, 'Dealer', None)]
		for you in self.players:
			winners.append((sum(you.hand), you.name, you)) 
		winners.sort()
		# print(winners)
		return winners


	def betting_round(self):
		playing = []
		for you in self.players:
			playing.append(you)
		# For all of the people in the game, get betting
		for you in self.players:
			you.initial_bet()

		# While there are people still wanting to play, 
		while len(playing) > 0:
			# Check all players for status
			for you in self.players:
				# Make sure they're still in
				if you not in playing:
					pass
				# If they are playing, check if hit
				elif you.hit():
					# Deal card on hit
					bust = you.deal_card(self.deck.draw())
					if bust:
						playing.remove(you)
				else:
					playing.remove(you)

		# Dealers Turn once everyone has played
		while sum(self.dealerUp)+self.__dealerDownCard < 16:
			self.dealerUp.append(self.deck.draw())


	def wrap_up(self, scores):
		# Complete the game an print all of the money won by player names.
		losers = []
		winners = []
		dealerScore = sum(self.dealerUp)+self.__dealerDownCard
		for you in scores:
			if you[0] == 21 and you[0] >= dealerScore:
				# Blackjack! Give them their money back
				if you[2] is None:
					pass
				else:
					you[2].won_money(1.5)
				winners.append(you)
			elif you[0] < 21 and you[0] >= dealerScore:
				# You still won, just less money
				if you[2] is None:
					pass
				else:
					you[2].won_money(1)
				winners.append(you)
			else:
				losers.append(you)

		# Print stuff
		# print("Winners!")
		# print(winners)
		# print("Losers")
		# print(losers)

		# Remove cards from the Dealer
		self.dealerUp = []
		self.__dealerDownCard = None



if __name__ == '__main__':
	t = Table()
	t.add_player(Player('Kevin', HumanPlayer))
	t.add_player(Player('Alice', HumanPlayer))
	t.add_player(Player('Josh', Gambit))
	for _ in range(100):
		t.game()

	print("Winnings:")
	t.players.sort(reverse=True, key=lambda x: x.bank)
	for you in t.players:
		print(you.name, you.bank)		
	