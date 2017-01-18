# Copyright 2017
# Simon de Bakker, Raoul van Duivenvoorde, Jeroen de Schepper

import pygame
import sys

green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 64, 128)

class Intro:
    def __init__ (self, width, height):
        self.Background = pygame.image.load("Background.jpg")
        self.Background = pygame.transform.scale(self.Background, (width, height))
        self.exit_button = Button('Exit', (width/10), (height/1.25), 170, 50)
        self.tutorial_button = Button('Tutorial', (width/10), (height/1.4), 170, 50)
        self.highscore_button = Button('Highscore', (width/10), (height/1.6), 170, 50)
        self.start_button = Button('Start', (width/10), (height/1.86), 170, 50)
    def update (self):
        pass
    def draw (self, screen):
        screen.blit(self.Background,(0, 0))
        self.exit_button.draw(screen)
        self.tutorial_button.draw(screen)
        self.highscore_button.draw(screen)
        self.start_button.draw(screen) 

class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.x = x
        self.y = y
        self.surface = pygame.Surface((w, h))
    def update(self):
        pass
    def draw (self, screen):
        screen.blit(self.surface, (self.x, self.y))
        
# Handle pygame events
def process_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           sys.exit()

    
# Main program logic
def program():
    width = 1280
    height = 720
    size = (width, height)
    
    # Start PyGame
    pygame.init()
    
    # Set the resolution
    screen = pygame.display.set_mode(size)

    intro = Intro(width, height) 
    
    while not process_events():   
        intro.draw(screen)
        # Flip the screen
        pygame.display.flip()
"""    mouse = pygame.mouse.get_pos()
       
    x = width/10
    y = height/1.25
    exit_button = pygame.Surface((170, 50))
    if x + 170 > mouse[0] > x and y + 50 > mouse[1] > y:
        exit_button.set_alpha(500)
        screen.blit(exit_button,(x, y))
    else: 
        exit_button.set_alpha(150)   
        screen.blit(exit_button,(x, y))
    
    y = height/1.4
    tutorial_button = pygame.Surface((170, 50))
    tutorial_button.set_alpha(150)
    screen.blit(tutorial_button,(x, y))

    y = height/1.6
    highscore_button = pygame.Surface((170, 50))
    highscore_button.set_alpha(150)
    screen.blit(highscore_button,(x, y))

    y = height/1.86
    start_button = pygame.Surface((170, 50))
    start_button.set_alpha(150)
    screen.blit(start_button,(x, y))
"""



# Start the program
program()

