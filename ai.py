#!/usr/bin/python

class HumanPlayer:
	"""This class is for a Human Player."""
	def __init__(self):
		pass
		
	def initial_bet(self):
		return 10

	def hit(self, cards):
		if sum(cards) > 17:
			return False
		else:
			return True

	def round_end(self, cards):
		pass


class Joshs_Pupil:
	"""This class is for a Human Player."""
	def __init__(self):
		pass
		
	def initial_bet(self):
		return 696969

	def hit(self, cards):
		if sum(cards) > 17:
			return False
		else:
			return True

	def round_end(self, cards):
		pass

class faggotfish:
	def __init__(self):
		pass
		
	def initial_bet(self):
		return 25

	def hit(self, cards):
		if sum(cards) > 17:
			return False
		else:
			return True

	def round_end(self, cards):
		pass


class RobertCalifornia:
	"""This class is for a Human Player."""
	def __init__(self):
		pass
		
	def initial_bet(self):
		return 30

	def hit(self, cards):
		if sum(cards) > 17:
			return False
		else:
			return True

	def round_end(self, cards):
		pass

class all_in:
	"""This class is for a Human Player."""
	def __init__(self):
		pass
		
	def initial_bet(self):
		return 1000000

	def hit(self, cards):
		if sum(cards) > 17:
			return False
		else:
			return True

	def round_end(self, cards):
		pass


class Gambit:
	counter = 0
	"""docstring for Gambit"""
	def __init__(self):
		self.counter = 0
	
	def initial_bet(self):
		return 10

	def hit(self, cards):
		if sum(cards) >= 17:
			return False
		elif sum(cards) > 15 and self.counter > -2:
			return False
		elif sum(cards) > 13 and self.counter > 0:
			return False
		if sum(cards) > 11 and self.counter > 2:
			return False
		else:
			return True

	def round_end(self, cards):
		# The smaller the number, the more low cards are in the deck
		# The larger the number, the more high cards are in the deck 
		for a in cards:
			if a.rank <= 6:
				self.counter += 1
			if a.rank >= 10	:
				self.counter -= 1


class Brennen:
	"""This class is for a Human Player."""
	def __init__(self):
		self.counter = 0

	def initial_bet(self):
		return 10
	def hit(self, cards):
		if sum(cards) > 15:
			return False
		else:
			return True
	def round_end(self, cards):
		pass
