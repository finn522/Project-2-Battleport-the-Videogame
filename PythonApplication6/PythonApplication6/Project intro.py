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
def mouse(x,y,w,h, button, screen):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[0] > y:
        button.set_alpha(550)
        screen.blit(button,(x, y))
    else: 
        button.set_alpha(150)   
        screen.blit(button,(x, y))
    
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
 
    xmouse, ymouse = pygame.mouse.get_pos()
    x = width/10
    y = height/1.25
    exit_button = pygame.Surface((170, 50))
    if x + 170 > xmouse > x and y + 50 > ymouse > y:
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

    while not process_events():   
        
        # Flip the screen
        pygame.display.flip()


# Start the program
program()

