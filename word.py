import pygame 

class Word:

    def __init__(self, time, text):
        self.time = time
        self.text = text
        self.surface = None
        self.on_screen = False
        self.pos = pygame.Rect(0,0,1,1)
        self.column = 0

    def __repr__(self):
        return "Word(" + str(self.time) + ", \"" + str(self.text) + "\")"
