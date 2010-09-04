from pygame import *

class Word:

	def __init__(self, time, text):
		self.time = time
		self.text = text
		self.surface = None
		self.on_screen = False
		self.pos = pygame.Rect(0,0,1,1)
