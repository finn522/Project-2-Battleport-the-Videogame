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
    width = 1280
    height = 720
    size = (width, height)
    
    # Start PyGame
    pygame.init()
    
    # Set the resolution
    Background = pygame.image.load("Background.jpg")
    Background = pygame.transform.scale(Background, (1280, 720))
    screen = pygame.display.set_mode(size)
    screen.blit(Background,(0, 0))

    while not process_events():   
        
        # Flip the screen
        pygame.display.flip()


# Start the program
program()