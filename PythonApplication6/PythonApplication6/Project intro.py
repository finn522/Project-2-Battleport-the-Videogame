# Copyright 2017
# Simon de Bakker, Raoul van Duivenvoorde, Jeroen de Schepper

import pygame
import sys

# Handle pygame events
def process_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           sys.exit()

# Main program logic
def program():
    width = 1680
    height = 980
    size = (width, height)
    
    # Start PyGame
    pygame.init()
    
    # Set the resolution
    Background = pygame.image.load("Background.jpg")
    screen = pygame.display.set_mode(size)
    screen.blit(Background,(-150, 0))

    while not process_events():   
        
        # Flip the screen
        pygame.display.flip()


# Start the program
program()