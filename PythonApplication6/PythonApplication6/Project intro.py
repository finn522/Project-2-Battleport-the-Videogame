# Copyright 2017
# Simon de Bakker, Raoul van Duivenvoorde, Jeroen de Schepper

import pygame
import sys

green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 64, 128)


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
    Background = pygame.image.load("Background.jpg")
    Background = pygame.transform.scale(Background, (size))
    screen = pygame.display.set_mode(size)
    screen.blit(Background,(0, 0))
    
    x = width/10
    y = height/1.25

    start_button = pygame.Surface((170, 50))
    start_button.set_alpha(150)
    screen.blit(start_button,(x, y))
    
    y = height/1.4
    tutorial_button = pygame.Surface((170, 50))
    tutorial_button.set_alpha(150)
    screen.blit(tutorial_button,(x, y))

    y = height/1.6
    exit_button = pygame.Surface((170, 50))
    exit_button.set_alpha(150)
    screen.blit(exit_button,(x, y))
    
    while not process_events():   
        
        # Flip the screen
        pygame.display.flip()


# Start the program
program()

