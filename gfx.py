
import pygame
from pygame.locals import *

class Display:

	def __init__(self):
		self.blitables = []
		self.screen = None
		self.bg_colour = (255,0,255)
		self.time = 0

	def init(self):
		pygame.init()
		self.screen = pygame.display.set_mode((640, 480))
		pygame.display.set_caption('Sweareoke!!')

	def title(self):
		# Fill background
		background = pygame.Surface(self.screen.get_size())
		background = background.convert()
		background.fill((255, 0, 255))

		# Display some text
		font = pygame.font.Font(None, 36)
		text = font.render("SWEAREOKE", 1, (255, 255, 255))
		textpos = text.get_rect()
		textpos.centerx = background.get_rect().centerx
		textpos.centery = background.get_rect().centery
		background.blit(text, textpos)

		self.blitables.append(background)
	
	def main(self, notes):
		# Fill background
		background = pygame.Surface(self.screen.get_size())
		background = background.convert()
		background.fill(bg_colour)
		
		notes.time

	def update(self, time)
		self.time = time

	def draw(self):
		# Blit everything to the screen
		for blitable in self.blitables:
			self.screen.blit(blitable, (0, 0))

		pygame.display.flip()


