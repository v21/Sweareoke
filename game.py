#!/usr/bin/python
from gfx import *
from word import *
import wrapperpykar
from random import randint
import sys

class Game:
    def __init__(self):
        self.run = True
        self.guitar = None

        self.level = 0
        self.time_window = 5000
        self.song_start_time = 0

        self.difficulty = 5
        self.error_margin = 500

        lyrics = wrapperpykar.parse_midi("american.kar")
        self.all_words = wrapperpykar.clean_syllables(lyrics)
        
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

        self.buttons_pressed = [False,False,False,False,False]

        self.buttons = [self.green, self.red, self.yellow, self.blue, self.orange]

    def init(self):
        self.display.init()
        self.display.load_title()
        self.guitar = pygame.joystick.Joystick(0)
        self.guitar.init()
        self.start_song()


    def start_song(self):
        self.song_start_time = pygame.time.get_ticks()
        for word in self.all_words:
            word.column = randint(0, self.difficulty-1)
        self.display.load_main(self.all_words, self.difficulty)
    
    def respond_to_strum_off(self, column):
        self.buttons_pressed[column] = False

    def respond_to_strum(self, column):
        if (not self.buttons_pressed[column]):
            self.buttons_pressed[column] = True
            current_time = pygame.time.get_ticks() - self.song_start_time
            for word in self.all_words:
                if (word.column == column and 
                        word.time > current_time - self.error_margin and
                        word.time < current_time + self.error_margin):
                    self.display.correct(column)
                    return
            self.display.incorrect(column)
        

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
                for button in self.buttons:
                    column = self.sound_button_map[button]
                    if self.guitar.get_button(button):
                        if event.value == 0:
                            self.respond_to_strum_off(column)
                        else:
                            self.respond_to_strum(column)

                

    def main_loop(self):
        while (self.run):
            self.process_input()
            time = pygame.time.get_ticks() - self.song_start_time
            self.display.update(time)
            self.display.draw()
            pygame.time.wait(33)

if (__name__ == "__main__"):
    if (len(sys.argv) > 1):
        filename = sys.argv[1]
    else:
        filename = "american.kar"
    game = Game()
    game.all_words = wrapperpykar.clean_syllables(wrapperpykar.parse_midi(filename))
    game.init()
    game.main_loop()
