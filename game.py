#!/usr/bin/python
from gfx import *
from word import *
from forvo import *
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

        self.song = None
        self.word_sounds = {}

        self.difficulty = 5
        self.error_margin = 500

        self.all_words = []
        
        self.display = Display(self.time_window)
        self.forvo = ForvoLibrary()


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

        self.filename = ""

    def init(self):
        self.display.init()
        self.display.load_title()
        self.song = pygame.mixer.music.load(self.filename)
        if (pygame.joystick.get_count() > 0):
            self.guitar = pygame.joystick.Joystick(0)
            self.guitar.init()

        self.all_words = wrapperpykar.clean_syllables(wrapperpykar.parse_midi(self.filename))
        
        game.all_words = [game.all_words[i] for i in range(6)]
        for word in game.all_words:
            print word
        
        words = [word.text for word in self.all_words]
        filenames = self.forvo.queryAndFetchMultiple(words, True)
        for word in filenames:
            self.word_sounds[word] = pygame.mixer.Sound(filenames[word])

    def start_song(self):
        self.song_start_time = pygame.time.get_ticks()
        for word in self.all_words:
            word.column = randint(0, self.difficulty-1)
        self.display.load_main(self.all_words, self.difficulty)
        pygame.mixer.music.play()
    
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
                    word.hit = True
                    return
            self.display.incorrect(column)
       
    def check_words(self, time):
        if (self.level != 0):
            for word in self.all_words:
                if (word.time < time - self.error_margin and not word.hit):
                    word.hit = True
                    self.display.incorrect(word.column)

    def process_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.run = False
            elif event.type == KEYDOWN:
                if self.level == 0:
                    self.level = 1
                    self.start_song()

                elif event.key == K_y:
                    self.respond_to_strum(0)
                elif event.key == K_u:
                    self.respond_to_strum(1)
                elif event.key == K_i:
                    self.respond_to_strum(2)
                elif event.key == K_o:
                    self.respond_to_strum(3)
                elif event.key == K_p:
                    self.respond_to_strum(4)

                if event.key == K_ESCAPE:
                    self.run = False

            elif event.type == KEYUP:
                if self.level == 1:
                    if event.key == K_y:
                        self.respond_to_strum_off(0)
                    elif event.key == K_u:
                        self.respond_to_strum_off(1)
                    elif event.key == K_i:
                        self.respond_to_strum_off(2)
                    elif event.key == K_o:
                        self.respond_to_strum_off(3)
                    elif event.key == K_p:
                        self.respond_to_strum_off(4)

            elif event.type == JOYBUTTONDOWN:
                if event.button in self.buttons:
                    if self.level == 0:
                        self.level = 1
                        self.start_song()
                    else:
                        self.display.push_button(self.sound_button_map[event.button])
            elif event.type == JOYBUTTONUP:
                if event.button in self.buttons:
                    self.display.unpush_button(self.sound_button_map[event.button])
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
            self.check_words(time)
            self.display.update(time)
            self.display.draw()
            pygame.time.wait(33)

if (__name__ == "__main__"):
    game = Game()

    if (len(sys.argv) > 1):
        game.filename = sys.argv[1]
    else:
        game.filename = "american.kar"

    game.init()
    game.main_loop()
