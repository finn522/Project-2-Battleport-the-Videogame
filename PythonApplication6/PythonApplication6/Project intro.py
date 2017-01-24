# Copyright 2017
# Simon de Bakker, Raoul van Duivenvoorde, Jeroen de Schepper

import pygame
from pygame.locals import*
import sys
import math

class Application:
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.size = (self.width, self.height)
    
        pygame.init()
    
        self.screen = pygame.display.set_mode((self.size))#, pygame.FULLSCREEN)
        self.phase = "intro"
        self.intro = Intro(self, self.width, self.height)
        self.game = Game(self, self.width, self.height)
        self.highscore = Highscore(self, self.width, self.height)
        self.tutorial = Tutorial(self, self.width, self.height)
        self.pause = Pause(self, self.width, self.height)
        
    def back(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    self.application.phase = "intro"
    
    def exit(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_BACKSPACE or event.key == K_p:
                    self.application.phase = "pause"

    def application_loop(self):
        while not process_events():
            if self.phase == "intro":
                self.intro.draw(self.screen)
            elif self.phase == "game":
                self.game.draw(self.screen)
            elif self.phase == "pause":
                self.pause.draw(self.screen)
            elif self.phase == 'Highscore':
                self.highscore.draw(self.screen) 
            elif self.phase == 'Tutorial':
                self.tutorial.draw(self.screen)
            pygame.display.flip()

class Intro:
    def __init__ (self, application, width, height):
        self.application = application
        self.Background = pygame.image.load("BackgroundA.jpg") #easteregg
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
        screen.blit(title_text,((self.width / 15) , (self.height / 9)))
        self.exit_button.mouse_action(screen)
        self.tutorial_button.mouse_action(screen)
        self.highscore_button.mouse_action(screen)
        self.start_button.mouse_action(screen)

class Button:
    def __init__(self, application, text, x, y, w, h):
        self.application = application
        self.text = text
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.surface = pygame.Surface((w, h))
        
    def mouse_action (self, screen):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.MOUSEBUTTONDOWN

        if self.application.phase == "intro":
            self.font = pygame.font.Font(None, 45)
            if self.x + self.w > mouse_pos[0] > self.x and self.y + self.h > mouse_pos[1] > self.y:
                button_text = self.font.render(self.text, 1, (255,255,255))
                screen.blit(button_text,(( self.x + 5), (self.y + 11)))

                for event in pygame.event.get():
                    if event.type == mouse_click:
                        print (self.text)
                        if self.text == 'Start':
                            self.application.phase = "game"
                        elif self.text == 'Tutorial':
                            self.application.phase = 'Tutorial'
                        elif self.text == 'Highscore':
                            self.application.phase = "Highscore"
                        elif self.text == 'Exit':
                            sys.exit()
            
            else:
                button_text = self.font.render(self.text, 1, (255,120,0))
                screen.blit(button_text,((self.x + 5), (self.y + 11)))

        if self.application.phase == "game":
            self.font = pygame.font.Font(None, 35)
            self.application.game.turn.current_turn(screen)
            if self.x + self.w > mouse_pos[0] > self.x and self.y + self.h > mouse_pos[1] > self.y:
                button_text = self.font.render(self.text, 1, (255,255,255))
                screen.blit(button_text,((self.x + 5), (self.y + 11)))
                for event in pygame.event.get():
                    if event.type == mouse_click:
                        print(self.text)
                        if self.text == 'Pause/Exit':
                            self.application.phase = "pause"                        
                        if self.text == "End Turn":
                            print(self.application.game.turn.turn)
                            self.application.game.turn.turn += 1
                        if self.text == 'Tutorial':
                            self.application.phase = "Tutorial"
            else:
                button_text = self.font.render(self.text, 1, (255,120,0))
                screen.blit(button_text,((self.x + 5), (self.y + 11)))
                                
        if self.application.phase == "pause":
            self.font = pygame.font.Font(None, 35)
            if self.x + self.w > mouse_pos[0] > self.x and self.y + self.h > mouse_pos[1] > self.y:
                button_text = self.font.render(self.text, 1, (255,255,255))
                screen.blit(button_text,((self.x + 5), (self.y + 11)))

                for event in pygame.event.get():
                    if event.type == mouse_click:
                        
                        print (self.text)
                        if self.text == '  Yes':
                            self.application.phase = "intro"
                        if self.text  == '   No':
                            self.application.phase = "game"
                        
            else:
                button_text = self.font.render(self.text, 1, (255,120,0))
                screen.blit(button_text,((self.x + 5), (self.y + 11)))
        
        if self.application.phase == "Highscore":
            self.font = pygame.font.Font(None, 45)
            if self.x + self.w > mouse_pos[0] > self.x and self.y + self.h > mouse_pos[1] > self.y:
                button_text = self.font.render(self.text, 1, (255,255,255))
                screen.blit(button_text,((self.x + 5), (self.y + 11)))

                for event in pygame.event.get():
                    if event.type == mouse_click:
                        print (self.text)
                        if self.text == 'Back to menu':
                            self.application.phase = "intro"
            else:
                button_text = self.font.render(self.text, 1, (255,120,0))
                screen.blit(button_text,((self.x + 5), (self.y + 11)))

        if self.application.phase == "Tutorial":
            self.font = pygame.font.Font(None, 45)
            if self.x + self.w > mouse_pos[0] > self.x and self.y + self.h > mouse_pos[1] > self.y:
                button_text = self.font.render(self.text, 1, (255,255,255))
                screen.blit(button_text,((self.x + 5), (self.y + 11)))
                for event in pygame.event.get():
                    if event.type == mouse_click:
                        print (self.text)
                        if self.text == "Back to menu":
                            self.application.phase = "intro"
                        if self.text == "Back to game / start game":
                            self.application.phase = "game"
            else:
                button_text = self.font.render(self.text, 1, (255,120,0))
                screen.blit(button_text,((self.x + 5), (self.y + 11)))
                
class Game:
    def __init__ (self, application, width, height):
        self.application = application
        self.pause = Pause
        self.width = width
        self.height = height
        self.turn = Turn(self.application, self.width, self.height)
        self.surface = pygame.Surface((width, height))
        self.Background = pygame.image.load("Speelbord.png")
        self.Background = pygame.transform.scale(self.Background, (width, height))
        self.font = pygame.font.SysFont('Arial', 150)

        self.player1 = Player(self.application, "Player 1")
        self.player2 = Player(self.application, "Player 2")

        self.end_turn_button = Button(self.application, ('End Turn'), (width/1.098), (height/1.615), 170, 65)        
        self.pause_button = Button(self.application, ('Pause/Exit'), (width/1.098), (height/1.112), 170, 65)
        self.tutorial_button = Button(self.application, ('Tutorial'), (width/1.098), (height/1.24), 170, 50) 

        self.sprites(self.width, self.height)
        self.boats(self.width, self.height)
        self.card(self.width, self.height)
        
    def sprites(self, width, height):
        # Sprites Lifepoints
        self.BattleshipHP     = pygame.image.load("BattleshipSprite.png")
        self.BattleshipHP     = pygame.transform.scale(self.BattleshipHP, (int(width / 7), int(height / 7)))
        self.Battleship4HP     = pygame.image.load("Battleship4HP.png")
        self.Battleship4HP     = pygame.transform.scale(self.Battleship4HP, (int(width / 7), int(height / 7)))
        self.Battleship3HP     = pygame.image.load("Battleship3HP.png")
        self.Battleship3HP     = pygame.transform.scale(self.Battleship3HP, (int(width / 7), int(height / 7)))
        self.Battleship2HP     = pygame.image.load("Battleship2HP.png")
        self.Battleship2HP     = pygame.transform.scale(self.Battleship2HP, (int(width / 7), int(height / 7)))
        self.Battleship1HP     = pygame.image.load("Battleship1HP.png")
        self.Battleship1HP     = pygame.transform.scale(self.Battleship1HP, (int(width / 7), int(height / 7)))
        self.Battleship0HP     = pygame.image.load("Battleship0HP.png")
        self.Battleship0HP     = pygame.transform.scale(self.Battleship0HP, (int(width / 7), int(height / 7)))

        self.DestroyerHP      = pygame.image.load("DestroyerSprite.png")
        self.DestroyerHP      = pygame.transform.scale(self.DestroyerHP, (int(width / 7), int(height / 7)))
        self.Destroyer3HP      = pygame.image.load("Destroyer3HP.png")
        self.Destroyer3HP      = pygame.transform.scale(self.Destroyer3HP, (int(width / 7), int(height / 7)))
        self.Destroyer2HP      = pygame.image.load("Destroyer2HP.png")
        self.Destroyer2HP      = pygame.transform.scale(self.Destroyer2HP, (int(width / 7), int(height / 7)))
        self.Destroyer1HP      = pygame.image.load("Destroyer1HP.png")
        self.Destroyer1HP      = pygame.transform.scale(self.Destroyer1HP, (int(width / 7), int(height / 7)))
        self.Destroyer0HP      = pygame.image.load("Destroyer0HP.png")
        self.Destroyer0HP      = pygame.transform.scale(self.Destroyer0HP, (int(width / 7), int(height / 7)))

        self.GunboatHP        = pygame.image.load("GunboatSprite.png")
        self.GunboatHP        = pygame.transform.scale(self.GunboatHP, (int(width / 7), int(height / 7)))
        self.Gunboat2HP        = pygame.image.load("Gunboat2HP.png")
        self.Gunboat2HP        = pygame.transform.scale(self.Gunboat2HP, (int(width / 7), int(height / 7)))
        self.Gunboat1HP        = pygame.image.load("Gunboat1HP.png")
        self.Gunboat1HP        = pygame.transform.scale(self.Gunboat1HP, (int(width / 7), int(height / 7)))
        self.Gunboat0HP        = pygame.image.load("Gunboat0HP.png")
        self.Gunboat0HP        = pygame.transform.scale(self.Gunboat0HP, (int(width / 7), int(height / 7)))
        
        # Sprites Attack & Movepoints
        self.AttPoint      = pygame.image.load("AttackPoint.png")
        self.AttPoint      = pygame.transform.scale(self.AttPoint, (62, 62))
        self.MovePoint     = pygame.image.load("Movepoint.png")
        self.MovePoint     = pygame.transform.scale(self.MovePoint, (62, 62))
        
        self.ShipMovePushed = pygame.image.load("Move_Button_Pushed.png")
        self.ShipMovePushed = pygame.transform.scale(self.ShipMovePushed, (62, 62))
        self.ShipDefPushed = pygame.image.load("Def_Button_Pushed.png")
        self.ShipDefPushed = pygame.transform.scale(self.ShipDefPushed, (62, 62))
        self.ShipAttPushed = pygame.image.load("Att_Button_Pushed.png")
        self.ShipAttPushed = pygame.transform.scale(self.ShipAttPushed, (62, 62))

    def boats(self, width, height):
        self.width = width
        self.height = height
        self.Battleship = pygame.image.load("Battleship.png")
        self.Battleship = pygame.transform.scale(self.Battleship, (int(width / 31), int(height / 4.7)))
        self.Destroyer = pygame.image.load("Destroyer.png")
        self.Destroyer = pygame.transform.scale(self.Destroyer, (int(width / 24), int(height / 6.2)))
        self.Gunboat = pygame.image.load("Gunboat.png")
        self.Gunboat = pygame.transform.scale(self.Gunboat, (int(width / 15.8), int(height / 9.2)))        

        self.Battleship2 = pygame.image.load("BattleshipP2.png")
        self.Battleship2 = pygame.transform.scale(self.Battleship, (int(width / 31), int(height / 4.7)))
        self.Battleship2 = pygame.transform.rotate(self.Battleship2, (180))
        self.Destroyer2 = pygame.image.load("DestroyerP2.png")
        self.Destroyer2 = pygame.transform.scale(self.Destroyer, (int(width / 24), int(height / 6.2)))
        self.Destroyer2 = pygame.transform.rotate(self.Destroyer2, (180))
        self.Gunboat2 = pygame.image.load("GunboatP2.png")
        self.Gunboat2 = pygame.transform.scale(self.Gunboat, (int(width / 15.8), int(height / 9.2)))  
        self.Gunboat2 = pygame.transform.rotate(self.Gunboat2, (180))     

    def card(self, width, height):
        self.Backcard = pygame.image.load("Back.png")
        self.Backcard = pygame.transform.scale(self.Backcard, (int(width /10.95), int(height /3.65)))
        self.BackcardRotate = pygame.transform.rotate(self.Backcard, (-90))  

    def draw (self, screen):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        screen.blit(self.Background, (0,0))
        self.end_turn_button.mouse_action(screen)
        self.pause_button.mouse_action(screen)
        self.tutorial_button.mouse_action(screen)

        # Screen blit Attack & Movepoints
        screen.blit(self.AttPoint, (self.width/12, self.height/4.400))
        screen.blit(self.AttPoint, (self.width/12, self.height/1.750))
        screen.blit(self.AttPoint, (self.width/12, self.height/1.110))
        screen.blit(self.MovePoint, (self.width/7, self.height/1.750))
        screen.blit(self.MovePoint, (self.width/7, self.height/4.400))
        screen.blit(self.MovePoint, (self.width/7, self.height/1.110))

        # Screen blit life sprites
        self.HP(screen)
        
        # Screen blit topview boats player 1
        screen.blit(self.Battleship, (453.5, 571))
        screen.blit(self.Destroyer, (560, 610))
        screen.blit(self.Gunboat, (755, 645))

        # Screen blit topview boats player 2
        screen.blit(self.Battleship2, (457.6, 0))
        screen.blit(self.Destroyer2, (553, 0))
        screen.blit(self.Gunboat2, (756, 0))

        # Blit cards
        screen.blit(self.Backcard, (1015, 11))
        screen.blit(self.Backcard, (1147, 11))  
        screen.blit(self.BackcardRotate, (1043, 223))          

        if mouse_click[0]:
            if (self.width/86.5) + 55 > mouse_pos[0] > (self.width/86.5) and (self.height/26) + 55 > mouse_pos[1] > (self.height/26):
                screen.blit(self.ShipMovePushed, (self.width/86.5, self.height/26))
            if (self.width/86) + 55 > mouse_pos[0] > (self.width/86) and (self.height/7.6) + 55 > mouse_pos[1] > (self.height/7.6):
                screen.blit(self.ShipDefPushed, (self.width/86, self.height/7.6))  
            if (self.width/86) + 55 > mouse_pos[0] > (self.width/86) and (self.height/4.42) + 55 > mouse_pos[1] > (self.height/4.42):
                screen.blit(self.ShipAttPushed, (self.width/86, self.height/4.42))

            if (self.width/86) + 55 > mouse_pos[0] > (self.width/86) and (self.height/2.6) + 55 > mouse_pos[1] > (self.height/2.6):
                screen.blit(self.ShipMovePushed, (self.width/86, self.height/2.6))
            if (self.width/86) + 55 > mouse_pos[0] > (self.width/86) and (self.height/2.1) + 55 > mouse_pos[1] > (self.height/2.1):
                screen.blit(self.ShipDefPushed, (self.width/86, self.height/2.1))  
            if (self.width/86) + 55 > mouse_pos[0] > (self.width/86) and (self.height/1.755) + 55 > mouse_pos[1] > (self.height/1.755):
                screen.blit(self.ShipAttPushed, (self.width/86, self.height/1.755))

            if (self.width/92) + 55 > mouse_pos[0] > (self.width/92) and (self.height/1.401) + 55 > mouse_pos[1] > (self.height/1.401):
                screen.blit(self.ShipMovePushed, (self.width/92, self.height/1.401))
            if (self.width/92) + 55 > mouse_pos[0] > (self.width/92) and (self.height/1.242) + 55 > mouse_pos[1] > (self.height/1.242):
                screen.blit(self.ShipDefPushed, (self.width/92, self.height/1.242))  
            if (self.width/92) + 55 > mouse_pos[0] > (self.width/92) and (self.height/1.112) + 55 > mouse_pos[1] > (self.height/1.112):
                screen.blit(self.ShipAttPushed, (self.width/92, self.height/1.112))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE]:
            self.application.phase = "pause"
        Application.exit(self)

    def HP(self, screen):
        if self.application.game.turn.turn % 2 != 0:
            self.Cplayer = self.application.game.player1
        else:
            self.Cplayer = self.application.game.player2
        if self.Cplayer.boat1.LifePoints <= 5:
            screen.blit(self.BattleshipHP, (80,500))
            if self.Cplayer.boat1.LifePoints <= 4:
                screen.blit(self.Battleship4HP, (80,500))
                if self.Cplayer.boat1.LifePoints <= 3:
                    screen.blit(self.Battleship3HP, (80,500))
                    if self.Cplayer.boat1.LifePoints <= 2:
                        screen.blit(self.Battleship2HP, (80,500))
                        if self.Cplayer.boat1.LifePoints <= 1:
                            screen.blit(self.Battleship1HP, (80,500))
                            if self.Cplayer.boat1.LifePoints <= 0:
                                screen.blit(self.Battleship0HP, (80,500))
        if self.Cplayer.boat2.LifePoints <= 4:
            screen.blit(self.DestroyerHP, (80,235))
            if self.Cplayer.boat2.LifePoints <= 3:
                screen.blit(self.Destroyer3HP, (80,235))
                if self.Cplayer.boat2.LifePoints <= 2:
                    screen.blit(self.Destroyer2HP, (80,235))
                    if self.Cplayer.boat2.LifePoints <= 1:
                        screen.blit(self.Destroyer1HP, (80,235))
                        if self.Cplayer.boat2.LifePoints <= 0:
                            screen.blit(self.Destroyer0HP, (80,235))
        if self.Cplayer.boat3.LifePoints <= 3:
            screen.blit(self.GunboatHP, (80,23))
            if self.Cplayer.boat3.LifePoints <= 2:
                screen.blit(self.Gunboat2HP, (80,23))
                if self.Cplayer.boat3.LifePoints <= 1:
                    screen.blit(self.Gunboat1HP, (80,23))
                    if self.Cplayer.boat3.LifePoints <= 0:
                        screen.blit(self.Gunboat0HP, (80,23))
        
class cards:
    def __init__(self, application):
        self.application = application
        # Attack cards
        self.AttCard1 = pygame.image.load("Adv_Rifling.png")
        self.AttCard1 = pygame.transform.scale(self.AttCard1, (int(width /10.95), int(height /3.65)))
        self.AttCard2 = pygame.image.load("EMP_Shot.png")
        self.AttCard2 = pygame.transform.scale(self.AttCard2, (int(width /10.95), int(height /3.65)))
        self.AttCard3 = pygame.image.load("FMJ.png")
        self.AttCard3 = pygame.transform.scale(self.AttCard3, (int(width /10.95), int(height /3.65)))
        self.AttCard4 = pygame.image.load("Rifling.png")
        self.AttCard4 = pygame.transform.scale(self.AttCard4, (int(width /10.95), int(height /3.65)))
        # Deffence cards
        self.DeffCard1 = pygame.image.load("Sabotage.png")
        self.DeffCard1 = pygame.transform.scale(self.DeffCard1, (int(width /10.95), int(height /3.65)))
        self.DeffCard2 = pygame.image.load("Smokescreen.png")
        self.DeffCard2 = pygame.transform.scale(self.DeffCard2, (int(width /10.95), int(height /3.65)))
        self.DeffCard3 = pygame.image.load("Repair.png")
        self.DeffCard3 = pygame.transform.scale(self.DeffCard3, (int(width /10.95), int(height /3.65)))
        # Utility Cards
        self.UtiCard1 = pygame.image.load("Adrenaline.png")
        self.UtiCard1 = pygame.transform.scale(self.UtiCard1, (int(width /10.95), int(height /3.65)))
        self.UtiCard2 = pygame.image.load("Extra Fuel II.png")
        self.UtiCard2 = pygame.transform.scale(self.UtiCard2, (int(width /10.95), int(height /3.65)))
        self.UtiCard3 = pygame.image.load("Extra Fuel I.png")
        self.UtiCard3 = pygame.transform.scale(self.UtiCard3, (int(width /10.95), int(height /3.65)))
        self.UtiCard4 = pygame.image.load("Redraw.png")
        self.UtiCard4 = pygame.transform.scale(self.UtiCard4, (int(width /10.95), int(height /3.65)))
        self.UtiCard5 = pygame.image.load("Rally.png")
        self.UtiCard5 = pygame.transform.scale(self.UtiCard5, (int(width /10.95), int(height /3.65)))
        # Special cards
        self.SpecCard1 = pygame.image.load("Adrenaline.png")
        self.SpecCard1 = pygame.transform.scale(self.SpecCard1, (int(width /10.95), int(height /3.65)))
        self.SpecCard2 = pygame.image.load("Extra Fuel II.png")
        self.SpecCard2 = pygame.transform.scale(self.SpecCard2, (int(width /10.95), int(height /3.65)))
        self.SpecCard3 = pygame.image.load("Extra Fuel I.png")
        self.SpecCard3 = pygame.transform.scale(self.SpecCard3, (int(width /10.95), int(height /3.65)))
        self.SpecCard4 = pygame.image.load("Redraw.png")
        self.SpecCard4 = pygame.transform.scale(self.SpecCard4, (int(width /10.95), int(height /3.65)))
        self.SpecCard5 = pygame.image.load("Rally.png")
        self.SpecCard5 = pygame.transform.scale(self.SpecCard5, (int(width /10.95), int(height /3.65)))

    def random_normal_cards (self):
        self.list_of_cards = [self.AttCard1, self.AttCard2, self.AttCard3, self.AttCard4, self.DeffCard1, self.DeffCard2, self.DeffCard3, self.UtiCard1, self.UtiCard2, self.UtiCard3, self.UtiCard4, self.UtiCard5]
        self.card = random.choice(self.list_of_cards)
        screen.blit(self.card, (1147, 11)) 

    def random_special_cards (self):
        self.list_of_specialcards = [self.SpecCard1, self.SpecCard2, self.SpecCard3, self.SpecCard4, self.SpecCard5]
        self.specialcard = random.choice(self.list_of_specialcards)
        screen.blit(self.specialcard, (1147, 11)) 

class Turn:
    def __init__ (self, application, x, y):
        self.application = application
        self.turn = 1
        self.x = x
        self.y = y
        self.font2 = pygame.font.Font(None, 25)

    def current_turn(self, screen):
        self.current_player_text = self.font2.render(('Current:'), 1, (255, 120, 0))
        screen.blit(self.current_player_text, ((self.x / 1.093), (self.y / 1.890)))
        self.current_player_name = self.font2.render(('{}'.format(self.currentplayer())), 1, (255, 120, 0))
        screen.blit(self.current_player_name, ((self.x / 1.093), (self.y / 1.800)))
        self.currentturn = self.font2.render(('Turn: {}'.format(self.turn - 1)), 1, (255, 120, 0))
        screen.blit(self.currentturn, ((self.x / 1.093), (self.y / 1.720)))
      
    def currentplayer(self):  
        if self.turn % 2 != 0:
            return self.application.game.player1.name
        else:
            return self.application.game.player2.name

class Player:
    def __init__ (self, application, name):
        self.application = application
        self.name = name
        self.boat1 = Boats(self.application, '?', '?', 5, 4, 5, 'Battleship')
        self.boat2 = Boats(self.application, '?', '?', 4, 3, 4, 'Destroyer')
        self.boat3 = Boats(self.application, '?', '?', 3, 2, 3, 'Gunboat')        

class Boats:
    def __init__ (self, application, width, height, lifepoints, Attrange, Deffrange, type):
        self.application = application
        self.width = width
        self.height = height
        self.LifePoints = lifepoints
        self.Attrange = Attrange
        self.Deffrange = Deffrange
        self.type = type
        self.position = (self.width, self.height)
  
class Pause:
    def __init__ (self, application, width, height):
        self.application = application
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont('arial', 150)
        self.font1 = pygame.font.SysFont('arial', 50)

        self.Yes = Button(self.application, '  Yes', (self.width/2.75), (self.height/1.7), 100, 55)
        self.No  = Button(self.application, '   No', (self.width/1.82), (self.height/1.7), 100, 55)
        
    def draw(self, screen):
        title_text = self.font.render("Pause", 1, (255,120,0))
        screen.blit(title_text,((self.width / 2.8) , (self.height / 6)))
        title_text1 = self.font1.render("Do you want to quit the game?", 1, (255,120,0))
        screen.blit(title_text1,((self.width / 3.5) , (self.height / 2.5)))
        self.Yes.mouse_action(screen)
        self.No.mouse_action(screen)  
        
class Highscore:
    def __init__ (self, application, width, height):
        self.application = application
        self.Background = pygame.image.load("BackgroundA.jpg")
        self.Background = pygame.transform.scale(self.Background, (width, height))
        self.font = pygame.font.SysFont('Arial', 150)
        self.width = width
        self.height = height
        
        self.back_to_menu = Button(self.application, ('Back to menu'), (width/15), (height/1.25), 205, 40)

    def draw (self, screen):
        screen.blit(self.Background,(0,0))
        title_text = self.font.render("Highscore", 1, (255,120,0))
        screen.blit(title_text,((self.width / 15) , (self.height / 9)))
        self.back_to_menu.mouse_action(screen)
        Application.back(self)
    
class Tutorial:
    def __init__ (self, application, width, height):
        self.application = application
        self.Background = pygame.image.load("BackgroundA.jpg")
        self.Background = pygame.transform.scale(self.Background, (width, height))
        self.font = pygame.font.SysFont('Arial', 150)
        self.width = width
        self.height = height

        self.back_to_menu = Button(self.application, ("Back to menu"), (width/15), (height/1.25), 205, 40)
        self.back_to_game = Button(self.application, ("Back to game / start game"), (width/15), (height/1.4), 205, 40)

    def draw (self, screen):
        screen.blit(self.Background,(0,0))
        title_text = self.font.render("Tutorial", 1, (255,120,0))
        screen.blit(title_text,((self.width / 15) , (self.height / 9)))
        self.back_to_menu.mouse_action(screen)
        self.back_to_game.mouse_action(screen)
        Application.back(self)
          
def process_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

def program():
    application = Application()
    application.application_loop()

program()
