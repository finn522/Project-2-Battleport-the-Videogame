# Copyright 2017
# Simon de Bakker, Raoul van Duivenvoorde, Jeroen de Schepper

import pygame
from pygame.locals import*
import sys
import math


green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 64, 128)

class Application:
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.size = (self.width, self.height)
    
        # Start PyGame
        pygame.init()
    
        # Set the resolution
        self.screen = pygame.display.set_mode((self.size)) # pygame.FULLSCREEN)
    
        self.phase = "intro"

        self.intro = Intro(self, self.width, self.height)
        self.game = Game(self, self.width, self.height)

    def application_loop(self):
        while not process_events():
            if self.phase == "intro":
                self.intro.draw(self.screen)
            elif self.phase == "game":
                self.game.draw(self.screen)
            # Flip the screen
            pygame.display.flip()

class Intro:
    def __init__ (self, application, width, height):
        self.application = application
        self.Background = pygame.image.load("BackgroundA.jpg")#easteregg
        self.Background = pygame.transform.scale(self.Background, (width, height))
        self.font = pygame.font.SysFont('Arial', 150)
        self.exit_button = Button(self.application, 'Exit', (width/15), (height/1.25), 170, 50)
        self.tutorial_button = Button(self.application, 'Tutorial', (width/15), (height/1.4), 170, 50)
        self.highscore_button = Button(self.application, 'Highscore', (width/15), (height/1.6), 170, 50)
        self.start_button = Button(self.application, 'Start', (width/15), (height/1.86), 170, 50)
        self.width = width
        self.height = height
    def draw (self, screen):
        screen.blit(self.Background,(0, 0))
        title_text = self.font.render("BattlePort", 1, (255,120,0))
        screen.blit(title_text,((self.width / 15) , (self.height / 9) ))
        self.exit_button.draw(screen)
        self.tutorial_button.draw(screen)
        self.highscore_button.draw(screen)
        self.start_button.draw(screen)

class Button:
    def __init__(self, application, text, x, y, w, h):
        self.application = application
        self.text = text
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.surface = pygame.Surface((w, h))
        self.font = pygame.font.Font(None, 45)
        self.width = 1280
        self.heigth = 720
    def draw (self, screen):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if self.x + 170 > mouse_pos[0] > self.x and self.y + 50 > mouse_pos[1] > self.y:
            screen.blit(self.surface, (self.x, self.y))
            button_text = self.font.render(self.text, 1, (255,255,255))
            screen.blit(button_text,(( self.x + 5), (self.y + 11) ))
            if mouse_click[0]:
                print (self.text)
                if self.text == 'Start':
                    # start_game = Game(self.width, self.heigth).draw(screen)
                    self.application.phase = "game"
                elif self.text == 'Tutorial':
                    pass
                elif self.text == 'Highscore':
                    pass
                elif self.text == 'Exit':
                    sys.exit()
        else:
            screen.blit(self.surface, (self.x, self.y))
            button_text = self.font.render(self.text, 1, (255,120,0))
            screen.blit(button_text,(( self.x + 5), (self.y + 11) ))

class Game:
    def __init__ (self, application, width, height):
        self.application = application
        self.Background = pygame.image.load("BackgroundA.jpg")
        self.Background = pygame.transform.scale(self.Background, (width, height))
        self.font = pygame.font.SysFont('Arial', 150)
        self.width = width
        self.height = height
    def draw (self, screen):
        screen.blit(self.Background,(0,0))
        title_text = self.font.render("Game start", 1, (255,120,0))
        screen.blit(title_text,((self.width / 15) , (self.height / 9) ))

                
# Handle pygame events
def process_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           sys.exit()

    
# Main program logic
def program():
    application = Application()
    application.application_loop()


"""def toggle_fullscreen():
    screen = pygame.display.get_surface()
    tmp = screen.convert()
    caption = pygame.display.get_caption()
    cursor = pygame.mouse.get_cursor()  # Duoas 16-04-2007 
    
    w,h = screen.get_width(),screen.get_height()
    flags = screen.get_flags()
    bits = screen.get_bitsize()
    
    pygame.display.quit()
    pygame.display.init()
    
    screen = pygame.display.set_mode((w,h),flags^FULLSCREEN,bits)
    screen.blit(tmp,(0,0))
    pygame.display.set_caption(*caption)
 
    pygame.key.set_mods(0) #HACK: work-a-round for a SDL bug??
 
    pygame.mouse.set_cursor( *cursor )  # Duoas 16-04-2007
    
    return screen"""


# Start the program
program()
