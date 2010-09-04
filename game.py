#!/usr/bin/python
import gfx
from gfx import *

class Game:
	def __init__(self):
		self.display = Display()

	def init(self):
		self.display.init()
		self.display.title()

	
	def main_loop(self):
		while (True):
			self.display.draw()


game = Game()
game.init()
game.main_loop()
