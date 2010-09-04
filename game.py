#!/usr/bin/python
import gfx
from gfx import *
import word
from word import *

class Game:
	def __init__(self):
		self.run = True
		self.guitar = None

		self.level = 0
		self.time_window = 5000
		self.song_start_time = 0
		self.all_words = [
				Word(1000, "One") ,
				Word(2000, "Two")]

		self.display = Display(self.time_window)


		self.red = 1
		self.green = 5
		self.yellow = 0
		self.blue = 2
		self.orange = 3
		self.tip = 4
		self.start = 9
		self.select = 8

		self.sound_button_map = {
			self.green : 0,
			self.red : 1,
			self.yellow : 2,
			self.blue : 3,
			self.orange : 4
		}

		self.buttons = [self.green, self.red, self.yellow, self.blue, self.orange]

	def init(self):
		self.display.init()
		self.display.load_title()
		self.guitar = pygame.joystick.Joystick(0)
		self.guitar.init()


	def start_song(self):
		self.song_start_time = pygame.time.get_ticks()
		self.display.load_main(self.all_words)

	def process_input(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self.run = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.run = False
			elif event.type == JOYBUTTONDOWN:
				if self.level == 0:
					self.level = 1
					self.start_song()
			elif event.type == JOYAXISMOTION:
				if event.value != 0:
					for button in self.buttons:
						if self.guitar.get_button(self.sound_button_map[button]):
							print "BUTTON " + str(button)
				

	def main_loop(self):
		while (self.run):
			self.process_input()
			time = pygame.time.get_ticks() - self.song_start_time
			self.display.update(time)
			self.display.draw()
			pygame.time.wait(33)


game = Game()
game.init()
game.main_loop()
