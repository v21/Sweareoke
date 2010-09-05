
import pygame
from pygame.locals import *
from random import randint

class Picture:
    def __init__(self, surface, pos, time):
        self.surface = surface
        self.pos = pos
        self.time = time

class Display:

    def __init__(self, time_window):
        self.blitables = []
        self.words = []
        self.buttons_pressed = [False for x in range(5)]
        self.buttons = []
        self.screen = None
        self.bg_colour = (0,255,255)
        self.time = 0
        self.last_time = 0
        self.time_window = time_window
        self.time_text = None
        self.difficulty = 3
        self.bottom_offset = 40
        self.match_bar_height = 20
        self.button_colours = [
                (0,255,0),
                (255,0,0),
                (255, 255, 0),
                (0,0,255),
                (255,180,0)]

        self.correct_image = None
        self.incorrect_image = None
        self.pictures = []

    def make_buttons(self):
        buttons = []
        for i in range(5):
            button = pygame.Surface((float(self.screen.get_width())/float(7), self.match_bar_height)).convert()
            button.fill(self.button_colours[i])
            buttons.append(button)
        return buttons


    def init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption('Sweareoke!!')
        self.big_font = pygame.font.Font(None, 100)
        self.small_font = pygame.font.Font(None, 60)
        self.buttons = self.make_buttons()

        self.correct_image = pygame.image.load("images/correct.png")
        self.incorrect_image = pygame.image.load("images/incorrect.png")

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

    def push_button(self, column):
        self.buttons_pressed[column] = True

    def unpush_button(self, column):
        self.buttons_pressed[column] = False


    def correct(self, column):
        print "YEAHAHHAAH!" + str(column)
        self.pictures.append(Picture(
            self.correct_image, 
            (self.column_centre(column), self.screen.get_height() - self.bottom_offset),
            1000))

    def incorrect(self, column):
        print "NOONONONO!!" + str(column)
        self.pictures.append(Picture(
            self.incorrect_image, 
            (self.column_centre(column), self.screen.get_height() - self.bottom_offset),
            1000))

    def column_centre(self, column):
        return (float(self.screen.get_width())/float(7)) * float(column+1.5)

    def column_left(self, column):
        return (float(self.screen.get_width())/float(7)) * float(column+1)

    def load_main(self, words, difficulty):
        self.difficulty = difficulty
        self.clear()

        # Fill background
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill(self.bg_colour)

        self.blitables.append((background, (0,0)))

        #match line
        match_line = pygame.Surface((self.screen.get_width(), self.match_bar_height)).convert()
        match_line.fill((255,255,255))
        self.blitables.append((match_line, (0,self.screen.get_height()-self.bottom_offset)))

        #bowling alleys
        for i in range(0,6):
            alley = pygame.Surface((4, self.screen.get_height())).convert()
            alley.fill((255,255,255))
            self.blitables.append((alley, (self.column_left(i), 0)))
        
        self.words = words
        for word in words:
            colour = self.button_colours[word.column]
            word.surface = self.small_font.render(word.text, 1, colour)
            word.pos = word.surface.get_rect()
            word.pos.centerx = self.column_centre(word.column)

        self.time_text = self.big_font.render("0", 1, (255,255,255))
    
    def clear(self):
        self.blitables = []
        self.words = []

    def update(self, time):
        delta = time - self.last_time
        self.last_time = self.time
        self.time = time
        for word in self.words:
            if word.time >= time or word.time < time + self.time_window:
                word.pos.bottom = self.screen.get_height() - float(self.screen.get_height())/float(self.time_window) * float((word.time-time)) - self.bottom_offset
                word.on_screen = True
            else:
                word.on_screen = False

        for picture in self.pictures:
            picture.time -= delta

        self.pictures = [picture for picture in self.pictures if picture.time > 0]


        self.time_text = self.big_font.render(str(time), 1, (0, 0, 0))

    def draw(self):
        # Blit everything to the screen
        for blitable in self.blitables:
            self.screen.blit(blitable[0], blitable[1])

        self.screen.blit(self.time_text, (0,0))

        i = 0
        for button in self.buttons:
            if (self.buttons_pressed[i]):
                self.screen.blit(button, (self.column_left(i), self.screen.get_height() - self.bottom_offset))
            i += 1
        
        for picture in self.pictures:
            rect = picture.surface.get_rect()
            rect.center = picture.pos
            self.screen.blit(picture.surface, rect)
        
        for word in self.words:
            if word.on_screen:
                self.screen.blit(word.surface, word.pos)

        pygame.display.flip()


