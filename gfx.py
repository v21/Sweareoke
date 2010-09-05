
import pygame
from pygame.locals import *
from random import randint

class Display:

	def __init__(self, time_window):
		self.blitables = []
		self.words = []
		self.screen = None
		self.bg_colour = (0,255,255)
		self.time = 0
		self.time_window = time_window
		self.time_text = None
		self.difficulty = 3
		self.bottom_offset = 40

	def init(self):
		pygame.init()
		self.screen = pygame.display.set_mode((640, 480))
		pygame.display.set_caption('Sweareoke!!')
		self.big_font = pygame.font.Font(None, 100)
		self.small_font = pygame.font.Font(None, 60)

	def load_title(self):
		# Fill background
		background = pygame.Surface(self.screen.get_size())
		background = background.convert()
		background.fill((255, 0, 255))

		# Display some text
		text = self.big_font.render("SWEAREOKE", 1, (255, 255, 255))
		textpos = text.get_rect()
		textpos.centerx = background.get_rect().centerx
		textpos.centery = background.get_rect().centery
		background.blit(text, textpos)

		self.blitables.append((background, (0,0)))

	def correct(self, column):
		print "YEAHAHHAAH!" + str(column)
		a = None

	def incorrect(self, column):
		print "NOONONONO!!" + str(column)
		a = None

	def load_main(self, words, difficulty):
		self.difficulty = difficulty
		self.clear()

		# Fill background
		background = pygame.Surface(self.screen.get_size())
		background = background.convert()
		background.fill(self.bg_colour)

		self.blitables.append((background, (0,0)))

		#match line
		match_line = pygame.Surface((self.screen.get_width(), 20)).convert()
		match_line.fill((255,255,255))
		self.blitables.append((match_line, (0,self.screen.get_height()-self.bottom_offset)))
		
		self.words = words
		for word in words:
			colour = (0,0,0)
			if (word.column == 1):
				colour = (0,255,0)
			elif (word.column == 2):
				colour = (255,0,0)
			elif (word.column == 3):
				colour = (255, 255, 0)
			elif (word.column == 4):
				colour = (0,0,255)
			elif (word.column == 5):
				colour = (255,180,0)
			word.surface = self.small_font.render(word.text, 1, colour)
			word.pos = word.surface.get_rect()
			word.pos.centerx = (float(self.screen.get_width())/float(difficulty+2)) * float(word.column+1)

		self.time_text = self.big_font.render("0", 1, (255,255,255))
	
	def clear(self):
		self.blitables = []
		self.words = []

	def update(self, time):
		self.time = time
		for word in self.words:
			if word.time >= time or word.time < time + self.time_window:
				word.pos.bottom = self.screen.get_height() - float(self.screen.get_height())/float(self.time_window) * float((word.time-time)) - self.bottom_offset
				word.on_screen = True
			else:
				word.on_screen = False

		self.time_text = self.big_font.render(str(time), 1, (0, 0, 0))

	def draw(self):
		# Blit everything to the screen
		for blitable in self.blitables:
			self.screen.blit(blitable[0], blitable[1])
		for word in self.words:
			if word.on_screen:
				self.screen.blit(word.surface, word.pos)

		self.screen.blit(self.time_text, (0,0))
			

		pygame.display.flip()


