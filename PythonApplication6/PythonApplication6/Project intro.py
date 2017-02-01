# Copyright 2017
# Simon de Bakker, Raoul van Duivenvoorde, Jeroen de Schepper

from pygame.locals import*
import pygame, sys, math, random, psycopg2

class Application:
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.size = (self.width, self.height)
     
        pygame.init()

        pygame.display.set_caption('BattlePort')
        self.VicSound = pygame.mixer.Sound('BurkeBlack.wav')
        pygame.mixer.music.load('BGM.wav')
    
        self.screen = pygame.display.set_mode((self.size))#, pygame.FULLSCREEN)
        self.phase = "intro"
        self.intro = Intro(self, self.width, self.height)
        self.game = Game(self, self.width, self.height)
        self.highscore = Highscore(self, self.width, self.height)
        self.tutorial = Tutorial(self, self.width, self.height)
        self.pause = Pause(self, self.width, self.height)
        self.victory = Victory(self, self.width, self.height)
        self.database = Database(self, self.width, self.height)
        self.mousedown = False
        self.mouse_pos = pygame.mouse.get_pos()
        self.events = []
       
    def process_events(self):
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == QUIT:
                sys.exit()

    def back(self):
        for event in self.application.events:
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    self.application.phase = "intro"
    
    def exit(self):
        for event in self.application.events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_BACKSPACE or event.key == K_p:
                    self.application.phase = "pause"

    def application_loop(self):
        pygame.mixer.music.play(-1)
        while not self.process_events():
            if self.phase == "intro":
                self.intro.draw(self.screen)
                self.VicSound.stop()
                pygame.mixer.music.rewind()
                pygame.mixer.music.unpause()
            elif self.phase == "game":
                self.game.draw(self.screen)
            elif self.phase == "pause":
                self.pause.draw(self.screen)
            elif self.phase == 'Highscore':
                self.highscore.draw(self.screen) 
            elif self.phase == 'Tutorial':
                self.tutorial.draw(self.screen)
            elif self.phase == 'Victory':
                self.victory.draw(self.screen)
                pygame.mixer.music.pause()
                self.VicSound.play()
                self.VicSound.set_volume(0.2)
            pygame.display.flip()

class Intro:
    def __init__ (self, application, width, height):
        self.application = application
        self.Background = pygame.image.load("BackgroundA.jpg")
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
        self.reset = Reset(self.application)
        
    def mouse_action (self, screen):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.MOUSEBUTTONDOWN

        if self.application.phase == "intro":
            self.font = pygame.font.Font(None, 45)
            if self.x + self.w > mouse_pos[0] > self.x and self.y + self.h > mouse_pos[1] > self.y:
                button_text = self.font.render(self.text, 1, (255,255,255))
                screen.blit(button_text,(( self.x + 5), (self.y + 11)))

                for event in self.application.events:
                    if event.type == MOUSEBUTTONDOWN:
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
                for event in self.application.events:
                    if event.type == MOUSEBUTTONDOWN:
                        print(self.text)
                        if self.text == 'Pause/Exit':
                            self.application.phase = "pause"                        
                        if self.text == "End Turn":
                            self.application.game.Cplayer.boat1.Fuel = 80
                            self.application.game.Cplayer.boat2.Fuel = 80
                            self.application.game.Cplayer.boat3.Fuel = 80
                            self.application.game.Cplayer.boat1.AttPoints = 100
                            self.application.game.Cplayer.boat2.AttPoints = 100
                            self.application.game.Cplayer.boat3.AttPoints = 100
                            self.application.game.GunboatMovement = False
                            self.application.game.DestroyerMovement = False
                            self.application.game.BattleshipMovement = False
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

                for event in self.application.events:
                    if event.type == MOUSEBUTTONDOWN:
                        
                        print (self.text)
                        if self.text == '  Yes':
                            self.reset.reset()
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

                for event in self.application.events:
                    if event.type == MOUSEBUTTONDOWN:
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
                for event in self.application.events:
                    if event.type == MOUSEBUTTONDOWN:
                        print (self.text)
                        if self.text == "Back to menu":
                            self.application.phase = "intro"
                        if self.text == "Back to game / start game":
                            self.application.phase = "game"
                        if self.text == "Previous":
                            if self.application.tutorial.page > 1:
                                self.application.tutorial.page -= 1
                        if self.text == "Next":
                            if self.application.tutorial.page < 8:
                                self.application.tutorial.page += 1
            else:
                button_text = self.font.render(self.text, 1, (255,120,0))
                screen.blit(button_text,((self.x + 5), (self.y + 11)))

        if self.application.phase == "Victory":
            self.font = pygame.font.Font(None, 45)
            if self.x + self.w > mouse_pos[0] > self.x and self.y + self.h > mouse_pos[1] > self.y:
                button_text = self.font.render(self.text, 1, (255,255,255))
                screen.blit(button_text,(( self.x + 5), (self.y + 11)))

                for event in self.application.events:
                    if event.type == MOUSEBUTTONDOWN:
                        print (self.text)
                        if self.text == 'Replay':
                            self.reset.reset()
                            self.application.phase = "game"
                        elif self.text == "Back to menu":
                            self.reset.reset()
                            self.application.phase = "intro"
            
            else:
                button_text = self.font.render(self.text, 1, (255,120,0))
                screen.blit(button_text,((self.x + 5), (self.y + 11)))

class Game:
    def __init__(self, application, width, height):
        self.application = application
        self.pause = Pause
        self.width = width
        self.height = height
        self.turn = Turn(self.application, self.width, self.height)
        self.boats = Boats
        self.surface = pygame.Surface((width, height))
        self.Background = pygame.image.load("Speelbord.png")
        self.Background = pygame.transform.scale(self.Background, (width, height))
        self.font = pygame.font.SysFont('Arial', 150)
        self.font_name_text = pygame.font.SysFont('Arial', 18)
        self.font_FUEL = pygame.font.SysFont('Arial', 25)
        self.font_enemyhp = pygame.font.SysFont('Arial', 50)

        self.BattleshipMovement = False
        self.GunboatMovement = False
        self.DestroyerMovement = False

        # Set up te player
        self.player1 = Player(self.application, "Player 1")
        self.player2 = Player(self.application, "Player 2")

        # Set up the boats
        self.player1.boat1 = Boats(self.application, 453, 571, 5, 2, 4, 5, 'Battleship', 'Att', 1)
        self.player1.boat2 = Boats(self.application, 490, 610, 4, 3, 3, 4, 'Destroyer', 'Att', 1)
        self.player1.boat3 = Boats(self.application, 258, 645, 3, 5, 2, 3, 'Gunboat', 'Att', 1)

        self.player2.boat1 = Boats(self.application, 458, 0, 5, 2, 4, 5, 'Battleship', 'Att', 1)
        self.player2.boat2 = Boats(self.application, 482, 0, 4, 3, 3, 4, 'Destroyer', 'Att', 1)
        self.player2.boat3 = Boats(self.application, 258, 0, 3, 5, 2, 3, 'Gunboat', 'Att', 1)

        # The buttons in the game
        self.end_turn_button = Button(self.application, ('End Turn'), (width/1.098), (height/1.615), 170, 65)        
        self.pause_button = Button(self.application, ('Pause/Exit'), (width/1.098), (height/1.112), 170, 65)
        self.tutorial_button = Button(self.application, ('Tutorial'), (width/1.098), (height/1.24), 170, 50) 

        self.sprites(self.width, self.height)
        self.boat(self.width, self.height)
        self.ships_count (self.width, self.height)

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

    def boat(self, width, height):
        self.width = width
        self.height = height
        self.Battleship = pygame.image.load("Battleship.png")
        self.Battleship = pygame.transform.scale(self.Battleship, (int(width / 31), int(height / 4.7)))
        self.BattleshipR = pygame.transform.rotate(self.Battleship, (90))
        self.Destroyer = pygame.image.load("Destroyer.png")
        self.Destroyer = pygame.transform.scale(self.Destroyer, (int(width / 24), int(height / 6.2)))
        self.DestroyerR = pygame.transform.rotate(self.Destroyer, (90))
        self.Gunboat = pygame.image.load("Gunboat.png")
        self.Gunboat = pygame.transform.scale(self.Gunboat, (int(width / 15.8), int(height / 9.2)))
        self.GunboatR = pygame.transform.rotate(self.Gunboat, (90))

        self.Battleship2 = pygame.image.load("BattleshipP2.png")
        self.Battleship2 = pygame.transform.scale(self.Battleship2, (int(width / 31), int(height / 4.7)))
        self.Battleship2 = pygame.transform.rotate(self.Battleship2, (180))
        self.Battleship2R = pygame.transform.rotate(self.Battleship2, (90))
        self.Destroyer2 = pygame.image.load("DestroyerP2.png")
        self.Destroyer2 = pygame.transform.scale(self.Destroyer2, (int(width / 24), int(height / 6.2)))
        self.Destroyer2 = pygame.transform.rotate(self.Destroyer2, (180))
        self.Destroyer2R = pygame.transform.rotate(self.Destroyer2, (90))
        self.Gunboat2 = pygame.image.load("GunboatP2.png")
        self.Gunboat2 = pygame.transform.scale(self.Gunboat2, (int(width / 15.8), int(height / 9.2)))  
        self.Gunboat2 = pygame.transform.rotate(self.Gunboat2, (180))
        self.Gunboat2R = pygame.transform.rotate(self.Gunboat2, (90))

        self.BattleshipDES = pygame.image.load("BattleshipDes.png")
        self.BattleshipDES = pygame.transform.scale(self.BattleshipDES, (int(width / 31), int(height / 4.7)))
        self.BattleshipDESP2 = pygame.transform.rotate(self.BattleshipDES, (180))
        self.BattleshipDESR = pygame.transform.rotate(self.BattleshipDES, (90))
        self.BattleshipDESP2R = pygame.transform.rotate(self.BattleshipDESP2, (90))
        self.DestroyerDES = pygame.image.load("DestroyerDes.png")
        self.DestroyerDES = pygame.transform.scale(self.DestroyerDES, (int(width / 24), int(height / 6.2)))
        self.DestroyerDESP2 = pygame.transform.rotate(self.DestroyerDES, (180))
        self.DestroyerDESR = pygame.transform.rotate(self.DestroyerDES, (90))
        self.DestroyerDESP2R = pygame.transform.rotate(self.DestroyerDES, (90))
        self.GunboatDES = pygame.image.load("GunboatDes.png")
        self.GunboatDES = pygame.transform.scale(self.GunboatDES, (int(width / 15.8), int(height / 9.2)))  
        self.GunboatDESP2 = pygame.transform.rotate(self.GunboatDES, (180))
        self.GunboatDESR = pygame.transform.rotate(self.GunboatDES, (90)) 
        self.GunboatDESP2R = pygame.transform.rotate(self.GunboatDES, (90))    

        self.d_pad = pygame.image.load("d_pad grey.png")
        self.d_pad = pygame.transform.scale(self.d_pad, (int(width / 21), int(height / 12)))
    
    def ships_count(self, width, height):
        self.Ship_lost_p1 = pygame.image.load("Ship_Lost_P1.png")
        self.Ship_lost_p1 = pygame.transform.scale(self.Ship_lost_p1, (int(width /80), int(height /25)))
        self.Ship_rem_p1 = pygame.image.load("Ship_Rem_P1.png")
        self.Ship_rem_p1 = pygame.transform.scale(self.Ship_rem_p1, (int(width /80), int(height /25)))
        self.Ship_lost_p2 = pygame.image.load("Ship_Lost_P2.png")
        self.Ship_lost_p2 = pygame.transform.scale(self.Ship_lost_p2, (int(width /80), int(height /25)))
        self.Ship_rem_p2 = pygame.image.load("Ship_Rem_P2.png")
        self.Ship_rem_p2 = pygame.transform.scale(self.Ship_rem_p2, (int(width /80), int(height /25)))

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        screen.blit(self.Background, (0,0))
        self.end_turn_button.mouse_action(screen)
        self.pause_button.mouse_action(screen)
        self.tutorial_button.mouse_action(screen)

        # check current player
        if self.application.game.turn.turn % 2 != 0:
            self.Cplayer = self.application.game.player1
            self.Eplayer = self.application.game.player2
        else:
            self.Cplayer = self.application.game.player2
            self.Eplayer = self.application.game.player1

        # Go to winning screen
        if self.player1.boat1.LifePoints <= 0 and self.player1.boat2.LifePoints <= 0 and self.player1.boat3.LifePoints <= 0:
            self.DB = self.application.database.update(self.application.game.Cplayer.name)
            self.application.phase = 'Victory'
        elif self.player2.boat1.LifePoints <= 0 and self.player2.boat2.LifePoints <= 0 and self.player2.boat3.LifePoints <= 0:
            self.DB = self.application.database.update(self.application.game.Cplayer.name)
            self.application.phase = 'Victory'
        
        # Screen blit diamants
        self.blit_diamants(screen)
    
        # Screen blit Attack & Movepoints
        if self.application.game.Cplayer.boat3.AttPoints > 0 and self.application.game.Cplayer.boat3.LifePoints > 0:
            screen.blit(self.AttPoint, (self.width/12, self.height/4.400))
        if self.application.game.Cplayer.boat2.AttPoints > 0 and self.application.game.Cplayer.boat2.LifePoints > 0:
            screen.blit(self.AttPoint, (self.width/12, self.height/1.750))
        if self.application.game.Cplayer.boat1.AttPoints > 0 and self.application.game.Cplayer.boat1.LifePoints > 0:
            screen.blit(self.AttPoint, (self.width/12, self.height/1.110))

        if self.Cplayer.boat2.Fuel > 0 and self.application.game.Cplayer.boat2.LifePoints > 0:
            screen.blit(self.MovePoint, (self.width/7, self.height/1.750))
        if self.Cplayer.boat3.Fuel > 0 and self.application.game.Cplayer.boat3.LifePoints > 0:
            screen.blit(self.MovePoint, (self.width/7, self.height/4.400))
        if self.Cplayer.boat1.Fuel > 0 and self.application.game.Cplayer.boat1.LifePoints > 0:
            screen.blit(self.MovePoint, (self.width/7, self.height/1.110))

        # Screen blit life sprites
        self.HP(screen)
        self.HP2(screen)
        
        # Screen blit topview boats player 1 & 2
        self.boats.draw(self,screen)        

        # Left side play buttons / information
        if self.turn.turn > 2:
            # blit fuel
            self.blit_fuel (screen, self.Cplayer)
            for event in self.application.events:
                if event.type == MOUSEBUTTONDOWN:
                    # check wich button is pushed + actions
                    # Gunboat
                    if self.Cplayer.boat3.LifePoints > 0:
                        if (self.width/86.5) + 55 > mouse_pos[0] > (self.width/86.5) and (self.height/26) + 55 > mouse_pos[1] > (self.height/26):
                            screen.blit(self.ShipMovePushed, (self.width/86.5, self.height/26))
                            if self.Cplayer.boat3.Mode == 'Att':
                                self.GunboatMovement = True
                                self.DestroyerMovement = False
                                self.BattleshipMovement = False
                        if (self.width/86) + 55 > mouse_pos[0] > (self.width/86) and (self.height/7.6) + 55 > mouse_pos[1] > (self.height/7.6):
                            screen.blit(self.ShipDefPushed, (self.width/86, self.height/7.6))  
                            if self.Cplayer.boat3.Mode == 'Att':
                                self.Cplayer.boat3.Mode = 'Deff'
                                self.GunboatMovement = False
                            elif self.Cplayer.boat3.Mode == 'Deff':
                                self.Cplayer.boat3.Mode = 'Att'
                        if (self.width/86) + 55 > mouse_pos[0] > (self.width/86) and (self.height/4.42) + 55 > mouse_pos[1] > (self.height/4.42):
                            screen.blit(self.ShipAttPushed, (self.width/86, self.height/4.42))
                            if self.application.game.Cplayer.boat3.AttPoints > 0:
                                if self.Cplayer.boat3.Mode == 'Att':
                                    if self.Cplayer == self.application.game.player1:
                                        self.attackP1B3()
                                    elif self.Cplayer == self.application.game.player2:
                                        self.attackP2B3()
                                elif self.Cplayer.boat3.Mode == 'Deff':
                                    if self.Cplayer == self.application.game.player1:
                                        self.defenceP1B3()
                                    elif self.Cplayer == self.application.game.player2:
                                        self.defenceP2B3()
                                self.application.game.Cplayer.boat3.AttPoints -= 1
                                
                    # Destroyer
                    if self.Cplayer.boat2.LifePoints > 0 :
                        if (self.width/86) + 55 > mouse_pos[0] > (self.width/86) and (self.height/2.6) + 55 > mouse_pos[1] > (self.height/2.6):
                            screen.blit(self.ShipMovePushed, (self.width/86, self.height/2.6))
                            if self.Cplayer.boat2.Mode == 'Att':
                                self.DestroyerMovement = True
                                self.GunboatMovement = False
                                self.BattleshipMovement = False
                        if (self.width/86) + 55 > mouse_pos[0] > (self.width/86) and (self.height/2.1) + 55 > mouse_pos[1] > (self.height/2.1):
                            screen.blit(self.ShipDefPushed, (self.width/86, self.height/2.1))
                            if self.Cplayer.boat2.Mode == 'Att':
                                self.Cplayer.boat2.Mode = 'Deff'
                                self.DestroyerMovement = False
                            elif self.Cplayer.boat2.Mode == 'Deff':
                                self.Cplayer.boat2.Mode = 'Att'  
                        if (self.width/86) + 55 > mouse_pos[0] > (self.width/86) and (self.height/1.755) + 55 > mouse_pos[1] > (self.height/1.755):
                            screen.blit(self.ShipAttPushed, (self.width/86, self.height/1.755))
                            if self.application.game.Cplayer.boat2.AttPoints > 0:
                                if self.Cplayer.boat2.Mode == 'Att':
                                    if self.Cplayer == self.application.game.player1:
                                        self.attackP1B2()
                                    elif self.Cplayer == self.application.game.player2:
                                        self.attackP2B2()
                                elif self.Cplayer.boat2.Mode == 'Deff':
                                    if self.Cplayer == self.application.game.player1:
                                        self.defenceP1B2()
                                    elif self.Cplayer == self.application.game.player2:
                                        self.defenceP2B2()
                                self.application.game.Cplayer.boat2.AttPoints -= 1

                    # Battleship
                    if self.Cplayer.boat1.LifePoints > 0:
                        if (self.width/92) + 55 > mouse_pos[0] > (self.width/92) and (self.height/1.401) + 55 > mouse_pos[1] > (self.height/1.401):
                            screen.blit(self.ShipMovePushed, (self.width/92, self.height/1.401))
                            if self.Cplayer.boat1.Mode == 'Att':
                                self.BattleshipMovement = True
                                self.GunboatMovement = False
                                self.DestroyerMovement = False
                        if (self.width/92) + 55 > mouse_pos[0] > (self.width/92) and (self.height/1.242) + 55 > mouse_pos[1] > (self.height/1.242):
                            screen.blit(self.ShipDefPushed, (self.width/92, self.height/1.242))  
                            if self.Cplayer.boat1.Mode == 'Att':
                                self.Cplayer.boat1.Mode = 'Deff'
                                self.BattleshipMovement = False
                            elif self.Cplayer.boat1.Mode == 'Deff':
                                self.Cplayer.boat1.Mode = 'Att' 
                        if (self.width/92) + 55 > mouse_pos[0] > (self.width/92) and (self.height/1.112) + 55 > mouse_pos[1] > (self.height/1.112):
                            screen.blit(self.ShipAttPushed, (self.width/92, self.height/1.112))
                            if self.application.game.Cplayer.boat1.AttPoints > 0:
                                if self.Cplayer.boat1.Mode == 'Att':
                                    if self.Cplayer == self.application.game.player1:
                                        self.attackP1B1()
                                    elif self.Cplayer == self.application.game.player2:
                                        self.attackP2B1()
                                elif self.Cplayer.boat1.Mode == 'Deff':
                                    if self.Cplayer == self.application.game.player1:
                                        self.defenceP1B1()
                                    elif self.Cplayer == self.application.game.player2:
                                        self.defenceP2B1()
                                self.application.game.Cplayer.boat1.AttPoints -= 1

        if self.GunboatMovement == True:
            screen.blit(self.d_pad, (self.width / 82, self.height / 25))
            self.movement(screen, self.Cplayer)
        if self.DestroyerMovement == True:
            screen.blit(self.d_pad, (self.width / 82, self.height / 2.59))
            self.movement(screen, self.Cplayer)
        if self.BattleshipMovement == True:
            screen.blit(self.d_pad, (self.width / 86, self.height / 1.400))
            self.movement(screen, self.Cplayer)

        # Place the boats if it is turn 1 or 2
        if self.turn.turn == 1:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                self.player1.boat1.width -= 35.7
                if self.player1.boat1.width < 275:
                    self.player1.boat1.width = 275
            if keys[pygame.K_e]:
                self.player1.boat1.width += 35.7
                if self.player1.boat1.width > 953.3:
                    self.player1.boat1.width = 953.3
            if keys[pygame.K_a]:
                self.player1.boat2.width -= 35.7
                if self.player1.boat2.width < 275:
                    self.player1.boat2.width = 275
            if keys[pygame.K_d]:
                self.player1.boat2.width += 35.7
                if self.player1.boat2.width > 953.3:
                    self.player1.boat2.width = 953.3
            if keys[pygame.K_z]:
                 self.player1.boat3.width -= 35.7
                 if self.player1.boat3.width < 258:
                     self.player1.boat3.width = 258
            if keys[pygame.K_c]:
                self.player1.boat3.width += 35.7
                if self.player1.boat3.width > 935:
                    self.player1.boat3.width = 935
        if self.turn.turn == 2:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                self.player2.boat1.width -= 35.7
                if self.player2.boat1.width < 280:
                    self.player2.boat1.width = 280
            if keys[pygame.K_e]:
                self.player2.boat1.width += 35.7
                if self.player2.boat1.width > 957:
                    self.player2.boat1.width = 957
            if keys[pygame.K_a]:
                self.player2.boat2.width -= 35.7
                if self.player2.boat2.width < 268:
                    self.player2.boat2.width = 268
            if keys[pygame.K_d]:
                self.player2.boat2.width += 35.7
                if self.player2.boat2.width > 946:
                    self.player2.boat2.width = 946
            if keys[pygame.K_z]:
               self.player2.boat3.width -= 35.7
               if self.player2.boat3.width < 258:
                  self.player2.boat3.width = 258
            if keys[pygame.K_c]:
                self.player2.boat3.width += 35.7
                if self.player2.boat3.width > 935:
                    self.player2.boat3.width = 935

        # press backspace to go to the pause menu
        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE]:
            self.application.phase = "pause"
        Application.exit(self)

    def HP(self, screen):
        # check current player
        if self.application.game.turn.turn % 2 != 0:
            self.Cplayer = self.application.game.player1
        else:
            self.Cplayer = self.application.game.player2
        # blit health points
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

    def HP2(self, screen):
        self.current_player_text = self.font_enemyhp.render(("Enemy's fleet"), 1, (255, 120, 0))
        screen.blit(self.current_player_text, ((self.width / 1.25), (self.height / 30)))
        # check current player
        if self.application.game.turn.turn % 2 != 0:
            self.Eplayer = self.application.game.player2
        else:
            self.Eplayer = self.application.game.player1
        # blit health points
        if self.Eplayer.boat1.LifePoints <= 5:
            screen.blit(self.BattleshipHP, (1050,240))
            if self.Eplayer.boat1.LifePoints <= 4:
                screen.blit(self.Battleship4HP, (1050,240))
                if self.Eplayer.boat1.LifePoints <= 3:
                    screen.blit(self.Battleship3HP, (1050,240))
                    if self.Eplayer.boat1.LifePoints <= 2:
                        screen.blit(self.Battleship2HP, (1050,240))
                        if self.Eplayer.boat1.LifePoints <= 1:
                            screen.blit(self.Battleship1HP, (1050,240))
                            if self.Eplayer.boat1.LifePoints <= 0:
                                screen.blit(self.Battleship0HP, (1050,240))
        if self.Eplayer.boat2.LifePoints <= 4:
            screen.blit(self.DestroyerHP, (1050,150))
            if self.Eplayer.boat2.LifePoints <= 3:
                screen.blit(self.Destroyer3HP, (1050,150))
                if self.Eplayer.boat2.LifePoints <= 2:
                    screen.blit(self.Destroyer2HP, (1050,150))
                    if self.Eplayer.boat2.LifePoints <= 1:
                        screen.blit(self.Destroyer1HP, (1050,150))
                        if self.Eplayer.boat2.LifePoints <= 0:
                            screen.blit(self.Destroyer0HP, (1050,150))
        if self.Eplayer.boat3.LifePoints <= 3:
            screen.blit(self.GunboatHP, (1050,80))
            if self.Eplayer.boat3.LifePoints <= 2:
                screen.blit(self.Gunboat2HP, (1050,80))
                if self.Eplayer.boat3.LifePoints <= 1:
                    screen.blit(self.Gunboat1HP, (1050,80))
                    if self.Eplayer.boat3.LifePoints <= 0:
                        screen.blit(self.Gunboat0HP, (1050,80))

    def blit_diamants(self, screen):
        # names
        self.name_tekst = self.font_name_text.render(self.player1.name, 1, (255,120,0))
        screen.blit(self.name_tekst,((1165) , (520)))
        self.name_tekst2 = self.font_name_text.render(self.player2.name, 1, (255,120,0))
        screen.blit(self.name_tekst2,((1225) , (520)))
        # player 1
        if self.player1.boat1.LifePoints <= 0:
            screen.blit(self.Ship_lost_p1, (1195, 550))
        else:
            screen.blit(self.Ship_rem_p1 ,(1195, 550))
        if self.player1.boat2.LifePoints <= 0:
            screen.blit(self.Ship_lost_p1, (1180, 550))
        else:
            screen.blit(self.Ship_rem_p1 ,(1180, 550))
        if self.player1.boat3.LifePoints <= 0:
            screen.blit(self.Ship_lost_p1, (1165, 550))
        else:
            screen.blit(self.Ship_rem_p1 ,(1165, 550))
        # player 2
        if self.player2.boat1.LifePoints <= 0:
            screen.blit(self.Ship_lost_p2, (1225, 550))
        else:
            screen.blit(self.Ship_rem_p2 ,(1225, 550))
        if self.player2.boat2.LifePoints <= 0:
            screen.blit(self.Ship_lost_p2, (1240, 550))
        else:
            screen.blit(self.Ship_rem_p2 ,(1240, 550))
        if self.player2.boat3.LifePoints <= 0:
            screen.blit(self.Ship_lost_p2, (1255, 550))
        else:
            screen.blit(self.Ship_rem_p2 ,(1255, 550))

    def collision_player1(self, Cplayer, Eplayer):
        if self.player1.boat1.height - (self.height/5.6) < self.player2.boat1.height:
            self.player1.boat1.height += 35.7

    def attackP1B1(self):
        #Vertical
        if (self.player1.boat1.height - (self.height/5.6) - (35.7 * self.player1.boat1.Attrange)) < self.player2.boat1.height and self.player1.boat1.height >= self.player2.boat1.height and (self.player2.boat1.width >= (self.player1.boat1.width - 3)) and self.player2.boat1.width < (self.player1.boat1.width + 20):
            self.player2.boat1.LifePoints -= 1
        if (self.player1.boat1.height - (self.height/5.6) - (35.7 * self.player1.boat1.Attrange)) < (self.player2.boat2.height - 35.7) and self.player1.boat1.height >= self.player2.boat2.height and (self.player2.boat2.width >= (self.player1.boat1.width - 10)) and self.player2.boat2.width < (self.player1.boat1.width + 20):
            self.player2.boat2.LifePoints -= 1
        if (self.player1.boat1.height - (self.height/5.6) - (35.7 * self.player1.boat1.Attrange)) < (self.player2.boat3.height - 71.4) and self.player1.boat1.height >= self.player2.boat3.height and (self.player2.boat3.width >= (self.player1.boat1.width - 20)) and self.player2.boat3.width < (self.player1.boat1.width + 10):
            self.player2.boat3.LifePoints -= 1

        #Horizontal
        if self.player1.boat1.height - (self.height/5.6) <= self.player2.boat1.height and (self.player1.boat1.height + (self.height/5.6)) >= self.player2.boat1.height and (35.7 * (self.player1.boat1.Attrange + 1)) + self.player1.boat1.width > self.player2.boat1.width and self.player1.boat1.width - (35.7 * self.player1.boat1.Attrange) < self.player2.boat1.width:
           self.player2.boat1.LifePoints -= 1
        if self.player1.boat1.height - (self.height/5.6) + 35.7 <= self.player2.boat2.height and (self.player1.boat1.height + (self.height/5.6)) >= self.player2.boat2.height and (35.7 * self.player1.boat1.Attrange) + self.player1.boat1.width > self.player2.boat2.width and self.player1.boat1.width - (35.7 * (self.player1.boat1.Attrange + 1)) < self.player2.boat2.width:
           self.player2.boat2.LifePoints -= 1
        if self.player1.boat1.height - (self.height/5.6) + 71.4 <= self.player2.boat3.height and (self.player1.boat1.height + (self.height/5.6)) >= self.player2.boat3.height and (35.7 * self.player1.boat1.Attrange -1) + self.player1.boat1.width > self.player2.boat3.width and self.player1.boat1.width - (35.7 * (self.player1.boat1.Attrange + 1)) < self.player2.boat3.width:
           self.player2.boat3.LifePoints -= 1

    def attackP1B2(self):
        #Vertical
        if (self.player1.boat2.height - (self.height/5.6) - (35.7 * self.player1.boat2.Attrange)) < self.player2.boat1.height and self.player1.boat2.height >= self.player2.boat1.height and (self.player2.boat1.width >= (self.player1.boat2.width - 3)) and self.player2.boat1.width < (self.player1.boat2.width + 20):
            self.player2.boat1.LifePoints -= 1
        if (self.player1.boat2.height - (self.height/5.6) - (35.7 * self.player1.boat2.Attrange)) < (self.player2.boat2.height - 35.7) and self.player1.boat2.height >= self.player2.boat2.height and (self.player2.boat2.width >= (self.player1.boat2.width - 10)) and self.player2.boat2.width < (self.player1.boat2.width + 20):
            self.player2.boat2.LifePoints -= 1
        if (self.player1.boat2.height - (self.height/5.6) - (35.7 * self.player1.boat2.Attrange)) < (self.player2.boat3.height - 71.4) and self.player1.boat2.height >= self.player2.boat3.height and (self.player2.boat3.width >= (self.player1.boat2.width - 20)) and self.player2.boat3.width < (self.player1.boat2.width + 10):
            self.player2.boat3.LifePoints -= 1

        #Horizontal
        if self.player1.boat2.height - (self.height/5.6) <= self.player2.boat1.height and (self.player1.boat2.height + (self.height/5.6)) - 35.7 >= self.player2.boat1.height and (35.7 * (self.player1.boat2.Attrange + 1)) + self.player1.boat2.width > self.player2.boat1.width and self.player1.boat2.width - (35.7 * self.player1.boat2.Attrange) < self.player2.boat1.width:
           self.player2.boat1.LifePoints -= 1
        if self.player1.boat2.height - (self.height/5.6) + 35.7 <= self.player2.boat2.height and (self.player1.boat2.height + (self.height/5.6)) - 35.7 >= self.player2.boat2.height and (35.7 * self.player1.boat2.Attrange) + self.player1.boat2.width > self.player2.boat2.width and self.player1.boat2.width - (35.7 * (self.player1.boat2.Attrange + 1)) < self.player2.boat2.width:
           self.player2.boat2.LifePoints -= 1
        if self.player1.boat2.height - (self.height/5.6) + 71.4 <= self.player2.boat3.height and (self.player1.boat2.height + (self.height/5.6)) - 35.7 >= self.player2.boat3.height and (35.7 * self.player1.boat2.Attrange -1) + self.player1.boat2.width > self.player2.boat3.width and self.player1.boat2.width - (35.7 * (self.player1.boat2.Attrange + 1)) < self.player2.boat3.width:
           self.player2.boat3.LifePoints -= 1

    def attackP1B3(self):
        #Vertical
        if (self.player1.boat3.height - (self.height/5.6) - (35.7 * self.player1.boat3.Attrange)) < self.player2.boat1.height and self.player1.boat3.height >= self.player2.boat1.height and (self.player2.boat1.width >= (self.player1.boat3.width - 3)) and self.player2.boat1.width < (self.player1.boat3.width + 30):
            self.player2.boat1.LifePoints -= 1
        if (self.player1.boat3.height - (self.height/5.6) - (35.7 * self.player1.boat3.Attrange)) < (self.player2.boat2.height - 35.7) and self.player1.boat3.height >= self.player2.boat2.height and (self.player2.boat2.width >= (self.player1.boat3.width - 10)) and self.player2.boat2.width < (self.player1.boat3.width + 20):
            self.player2.boat2.LifePoints -= 1
        if (self.player1.boat3.height - (self.height/5.6) - (35.7 * self.player1.boat3.Attrange)) < (self.player2.boat3.height - 71.4) and self.player1.boat3.height >= self.player2.boat3.height and (self.player2.boat3.width >= (self.player1.boat3.width - 20)) and self.player2.boat3.width < (self.player1.boat3.width + 10):
            self.player2.boat3.LifePoints -= 1

        #Horizontal
        if self.player1.boat3.height - (self.height/5.6) <= self.player2.boat1.height and (self.player1.boat3.height + (self.height/5.6)) - 71.4 >= self.player2.boat1.height and (35.7 * (self.player1.boat3.Attrange + 1)) + self.player1.boat3.width > self.player2.boat1.width and self.player1.boat3.width - (35.7 * self.player1.boat3.Attrange) < self.player2.boat1.width:
           self.player2.boat1.LifePoints -= 1
        if self.player1.boat3.height - (self.height/5.6) + 35.7 <= self.player2.boat2.height and (self.player1.boat3.height + (self.height/5.6)) - 71.4 >= self.player2.boat2.height and (35.7 * (self.player1.boat3.Attrange + 1)) + self.player1.boat3.width > self.player2.boat2.width and self.player1.boat3.width - (35.7 * (self.player1.boat3.Attrange)) < self.player2.boat2.width:
           self.player2.boat2.LifePoints -= 1
        if self.player1.boat3.height - (self.height/5.6) + 71.4 <= self.player2.boat3.height and (self.player1.boat3.height + (self.height/5.6)) - 71.4 >= self.player2.boat3.height and (35.7 * (self.player1.boat3.Attrange)) + self.player1.boat3.width > self.player2.boat3.width and self.player1.boat3.width - (35.7 * (self.player1.boat3.Attrange)) < self.player2.boat3.width:
           self.player2.boat3.LifePoints -= 1

    def attackP2B1(self):
        #Vertical
        if (self.player2.boat1.height + (self.height/5.6) + (35.7 * self.player2.boat1.Attrange)) > self.player1.boat1.height and self.player2.boat1.height <= self.player1.boat1.height and (self.player2.boat1.width >= (self.player1.boat1.width - 3)) and self.player2.boat1.width < (self.player1.boat1.width + 30):
            self.player1.boat1.LifePoints -= 1
        if (self.player2.boat1.height + (self.height/5.6) + (35.7 * self.player2.boat1.Attrange)) > self.player1.boat2.height and self.player2.boat1.height <= self.player1.boat2.height and (self.player2.boat1.width >= (self.player1.boat2.width - 10)) and self.player2.boat1.width < (self.player1.boat2.width + 20):
            self.player1.boat2.LifePoints -= 1
        if (self.player2.boat1.height + (self.height/5.6) + (35.7 * self.player2.boat1.Attrange)) > self.player1.boat3.height and self.player2.boat1.height <= self.player1.boat3.height and (self.player2.boat1.width >= (self.player1.boat3.width)) and self.player2.boat1.width < (self.player1.boat3.width + 30):
            self.player1.boat3.LifePoints -= 1

        #Horizontal
        if self.player2.boat1.height + (self.height/5.6) >= self.player1.boat1.height and (self.player2.boat1.height - (self.height/5.6)) <= self.player1.boat1.height and (35.7 * (self.player2.boat1.Attrange)) + self.player2.boat1.width > self.player1.boat1.width and self.player2.boat1.width - (35.7 * (self.player2.boat1.Attrange + 1)) < self.player1.boat1.width:
           self.player1.boat1.LifePoints -= 1
        if self.player2.boat1.height + (self.height/5.6) >= self.player1.boat2.height and (self.player2.boat1.height - (self.height/5.6) + 35.7) <= self.player1.boat2.height and (35.7 * (self.player2.boat1.Attrange)) + self.player2.boat1.width > self.player1.boat2.width and self.player2.boat1.width - (35.7 * (self.player2.boat1.Attrange + 1)) < self.player1.boat2.width:
           self.player1.boat2.LifePoints -= 1
        if self.player2.boat1.height + (self.height/5.6) >= self.player1.boat3.height and (self.player2.boat1.height - (self.height/5.6) + 71.4) <= self.player1.boat3.height and (35.7 * (self.player2.boat1.Attrange)) + self.player2.boat1.width > self.player1.boat3.width and self.player2.boat1.width - (35.7 * (self.player2.boat1.Attrange + 1)) < self.player1.boat3.width:
           self.player1.boat3.LifePoints -= 1

    def attackP2B2(self):
        #Vertical
        if (self.player2.boat2.height + (self.height/5.6) + (35.7 * self.player2.boat2.Attrange)) > (self.player1.boat1.height + 35.7) and self.player2.boat2.height <= self.player1.boat1.height and (self.player2.boat2.width >= (self.player1.boat1.width - 10)) and self.player2.boat2.width < (self.player1.boat1.width + 20):
            self.player1.boat1.LifePoints -= 1
        if (self.player2.boat2.height + (self.height/5.6) + (35.7 * self.player2.boat2.Attrange)) > (self.player1.boat2.height + 71.4) and self.player2.boat2.height <= self.player1.boat2.height and (self.player2.boat2.width >= (self.player1.boat2.width - 10)) and self.player2.boat2.width < (self.player1.boat2.width + 20):
            self.player1.boat2.LifePoints -= 1
        if (self.player2.boat2.height + (self.height/5.6) + (35.7 * self.player2.boat2.Attrange)) > (self.player1.boat3.height + 71.4) and self.player2.boat2.height <= self.player1.boat3.height and (self.player2.boat2.width >= (self.player1.boat3.width - 20)) and self.player2.boat2.width < (self.player1.boat3.width + 30):
            self.player1.boat3.LifePoints -= 1

        #Horizontal
        if self.player2.boat2.height + (self.height/5.6) - 35.7 >= self.player1.boat1.height and (self.player2.boat2.height - (self.height/5.6)) <= self.player1.boat1.height and (35.7 * (self.player2.boat2.Attrange + 1)) + self.player2.boat2.width > self.player1.boat1.width and self.player2.boat2.width - (35.7 * (self.player2.boat2.Attrange)) < self.player1.boat1.width:
           self.player1.boat1.LifePoints -= 1
        if self.player2.boat2.height + (self.height/5.6) - 35.7 >= self.player1.boat2.height and (self.player2.boat2.height - (self.height/5.6) + 35.7) <= self.player1.boat2.height and (35.7 * (self.player2.boat2.Attrange + 1)) + self.player2.boat2.width > self.player1.boat2.width and self.player2.boat2.width - (35.7 * (self.player2.boat2.Attrange)) < self.player1.boat2.width:
           self.player1.boat2.LifePoints -= 1
        if self.player2.boat2.height + (self.height/5.6) - 35.7 >= self.player1.boat3.height and (self.player2.boat2.height - (self.height/5.6) + 71.4) <= self.player1.boat3.height and (35.7 * (self.player2.boat2.Attrange)) + self.player2.boat2.width > self.player1.boat3.width and self.player2.boat2.width - (35.7 * (self.player2.boat2.Attrange + 1)) < self.player1.boat3.width:
           self.player1.boat3.LifePoints -= 1

    def attackP2B3(self):
        #Vertical
        if (self.player2.boat3.height + (self.height/5.6) + (35.7 * self.player2.boat3.Attrange)) > (self.player1.boat1.height + 71.4) and self.player2.boat3.height <= self.player1.boat1.height and (self.player2.boat3.width >= (self.player1.boat1.width - 20)) and self.player2.boat3.width < (self.player1.boat1.width + 10):
            self.player1.boat1.LifePoints -= 1
        if (self.player2.boat3.height + (self.height/5.6) + (35.7 * self.player2.boat3.Attrange)) > (self.player1.boat2.height + 71.4) and self.player2.boat3.height <= self.player1.boat2.height and (self.player2.boat3.width >= (self.player1.boat2.width - 20)) and self.player2.boat3.width < (self.player1.boat2.width + 10):
            self.player1.boat2.LifePoints -= 1
        if (self.player2.boat3.height + (self.height/5.6) + (35.7 * self.player2.boat3.Attrange)) > (self.player1.boat3.height + 71.4) and self.player2.boat3.height <= self.player1.boat3.height and (self.player2.boat3.width >= (self.player1.boat3.width - 20)) and self.player2.boat3.width < (self.player1.boat3.width + 10):
            self.player1.boat3.LifePoints -= 1

        #Horizontal
        if self.player2.boat3.height + (self.height/5.6) - 71.4 >= self.player1.boat1.height and (self.player2.boat3.height - (self.height/5.6)) <= self.player1.boat1.height and (35.7 * (self.player2.boat3.Attrange + 1)) + self.player2.boat3.width > self.player1.boat1.width and self.player2.boat3.width - (35.7 * (self.player2.boat3.Attrange)) < self.player1.boat1.width:
           self.player1.boat1.LifePoints -= 1
        if self.player2.boat3.height + (self.height/5.6) - 71.4 >= self.player1.boat2.height and (self.player2.boat3.height - (self.height/5.6) + 35.7) <= self.player1.boat2.height and (35.7 * (self.player2.boat3.Attrange + 1)) + self.player2.boat3.width > self.player1.boat2.width and self.player2.boat3.width - (35.7 * (self.player2.boat3.Attrange)) < self.player1.boat2.width:
           self.player1.boat2.LifePoints -= 1
        if self.player2.boat3.height + (self.height/5.6) - 71.4 >= self.player1.boat3.height and (self.player2.boat3.height - (self.height/5.6) + 71.4) <= self.player1.boat3.height and (35.7 * (self.player2.boat3.Attrange)) + self.player2.boat3.width > self.player1.boat3.width and self.player2.boat3.width - (35.7 * (self.player2.boat3.Attrange + 1)) < self.player1.boat3.width:
           self.player1.boat3.LifePoints -= 1

    def defenceP1B1(self):
        if (self.player1.boat1.height - (self.height/5.6) - (35.7 * (self.player1.boat1.Deffrange))) < self.player2.boat1.height and self.player1.boat1.height + (35.7 * self.player1.boat1.Deffrange + 35.7) >= self.player2.boat1.height and (self.player2.boat1.width >= (self.player1.boat1.width - 3)) and self.player2.boat1.width < (self.player1.boat1.width + int(self.height / 4.7) - 35.7):
            self.player2.boat1.LifePoints -= 1
        if (self.player1.boat1.height - (self.height/5.6) - (35.7 * (self.player1.boat1.Deffrange) - 35.7)) < self.player2.boat2.height and self.player1.boat1.height + (35.7 * self.player1.boat1.Deffrange + 35.7) >= self.player2.boat2.height and (self.player2.boat2.width >= (self.player1.boat1.width - 35.7)) and self.player2.boat2.width < (self.player1.boat1.width + int(self.height / 4.7) - 35.7):
            self.player2.boat2.LifePoints -= 1
        if (self.player1.boat1.height - (self.height/5.6) - (35.7 * (self.player1.boat1.Deffrange) - 71.4)) < self.player2.boat3.height and self.player1.boat1.height + (35.7 * self.player1.boat1.Deffrange + 35.7) >= self.player2.boat3.height and (self.player2.boat3.width >= (self.player1.boat1.width - 35.7)) and self.player2.boat3.width < (self.player1.boat1.width + int(self.height / 4.7) - 35.7):
            self.player2.boat3.LifePoints -= 1

    def defenceP1B2(self):
        if (self.player1.boat2.height - (self.height/5.6) - (35.7 * (self.player1.boat2.Deffrange))) < self.player2.boat1.height and self.player1.boat2.height + (35.7 * self.player1.boat2.Deffrange) >= self.player2.boat1.height and (self.player2.boat1.width >= (self.player1.boat2.width - 3)) and self.player2.boat1.width < (self.player1.boat2.width + int(self.height / 6.2) - 35.7):
            self.player2.boat1.LifePoints -= 1
        if (self.player1.boat2.height - (self.height/5.6) - (35.7 * (self.player1.boat2.Deffrange) - 35.7)) < self.player2.boat2.height and self.player1.boat2.height + (35.7 * self.player1.boat2.Deffrange) >= self.player2.boat2.height and (self.player2.boat2.width >= (self.player1.boat2.width - 35.7)) and self.player2.boat2.width < (self.player1.boat2.width + int(self.height / 6.2) - 35.7):
            self.player2.boat2.LifePoints -= 1
        if (self.player1.boat2.height - (self.height/5.6) - (35.7 * (self.player1.boat2.Deffrange) - 71.4)) < self.player2.boat3.height and self.player1.boat2.height + (35.7 * self.player1.boat2.Deffrange) >= self.player2.boat3.height and (self.player2.boat3.width >= (self.player1.boat2.width - 35.7)) and self.player2.boat3.width < (self.player1.boat2.width + int(self.height / 6.2) - 35.7):
            self.player2.boat3.LifePoints -= 1

    def defenceP1B3(self):
        if (self.player1.boat3.height - (self.height/5.6) - (35.7 * (self.player1.boat3.Deffrange))) < self.player2.boat1.height and self.player1.boat3.height + (35.7 * self.player1.boat3.Deffrange) >= self.player2.boat1.height and (self.player2.boat1.width >= (self.player1.boat3.width - 3)) and self.player2.boat1.width < (self.player1.boat3.width + int(self.height / 7) - 35.7):
            self.player2.boat1.LifePoints -= 1
        if (self.player1.boat3.height - (self.height/5.6) - (35.7 * (self.player1.boat3.Deffrange) - 35.7)) < self.player2.boat2.height and self.player1.boat3.height + (35.7 * self.player1.boat3.Deffrange) >= self.player2.boat2.height and (self.player2.boat2.width >= (self.player1.boat3.width - 3)) and self.player2.boat2.width < (self.player1.boat3.width + int(self.height / 7) - 35.7):
            self.player2.boat2.LifePoints -= 1
        if (self.player1.boat3.height - (self.height/5.6) - (35.7 * (self.player1.boat3.Deffrange) - 71.4)) < self.player2.boat3.height and self.player1.boat3.height + (35.7 * self.player1.boat3.Deffrange) >= self.player2.boat3.height and (self.player2.boat3.width >= (self.player1.boat3.width - 3)) and self.player2.boat3.width < (self.player1.boat3.width + int(self.height / 7) - 35.7):
            self.player2.boat3.LifePoints -= 1

    def defenceP2B1(self):
        if (self.player2.boat1.height + (35.7 * (self.player2.boat1.Deffrange))) > self.player1.boat1.height and self.player2.boat1.height - (self.height/5.6) - (35.7 * self.player2.boat1.Deffrange) <= self.player1.boat1.height and (self.player1.boat1.width >= (self.player2.boat1.width - 35.7)) and self.player1.boat1.width < (self.player2.boat1.width + int(self.height / 6.2) - 35.7):
            self.player1.boat1.LifePoints -= 1
        if (self.player2.boat1.height + (35.7 * (self.player2.boat1.Deffrange + 1))) > self.player1.boat2.height and self.player2.boat1.height - (self.height/5.6) - (35.7 * (self.player2.boat1.Deffrange - 1)) <= self.player1.boat2.height and (self.player1.boat2.width >= (self.player2.boat2.width) - 3) and self.player1.boat2.width < (self.player2.boat1.width + int(self.height / 6.2)):
            self.player1.boat2.LifePoints -= 1
        if (self.player2.boat1.height + (35.7 * (self.player2.boat1.Deffrange + 1))) > self.player1.boat3.height and self.player2.boat1.height - (self.height/5.6) - (35.7 * (self.player2.boat1.Deffrange - 2)) <= self.player1.boat3.height and (self.player1.boat3.width >= (self.player2.boat2.width) - 3) and self.player1.boat3.width < (self.player2.boat1.width + int(self.height / 6.2)):
            self.player1.boat3.LifePoints -= 1

    def defenceP2B2(self):
        pass
    def defenceP2B3(self):
        pass

    def movement(self, screen, Cplayer):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        for event in self.application.events:
            if event.type == MOUSEBUTTONDOWN:
                # Movement gunboat
                if self.GunboatMovement == True:
                    if self.Cplayer.boat3.Fuel > 0:
                            if (self.width/37) + 20 > mouse_pos[0] > (self.width/37) and (self.height/24) + 20 > mouse_pos[1] > (self.height/24):
                                self.Cplayer.boat3.height -= 35.7
                                if self.Cplayer.boat3.height < 0:
                                    self.Cplayer.boat3.height = 0
                                else: 
                                    self.Cplayer.boat3.Fuel -= 1
                            if (self.width/37) + 20 > mouse_pos[0] > (self.width/37) and (self.height/10.5) + 20 > mouse_pos[1] > (self.height/10.5):
                                self.Cplayer.boat3.height += 35.7
                                if self.Cplayer.boat3.height > 642:
                                    self.Cplayer.boat3.height = 642
                                else:
                                    self.Cplayer.boat3.Fuel -= 1
                            if (self.width/75) + 20 > mouse_pos[0] > (self.width/75) and (self.height/15) + 20 > mouse_pos[1] > (self.height/15):
                                self.Cplayer.boat3.width -= 35.7
                                if self.Cplayer.boat3.width < 257:
                                    self.Cplayer.boat3.width = 257
                                else:
                                    self.Cplayer.boat3.Fuel -= 1
                            if (self.width/23) + 20 > mouse_pos[0] > (self.width/23) and (self.height/15) + 20 > mouse_pos[1] > (self.height/15):
                                self.Cplayer.boat3.width += 35.7
                                if self.Cplayer.boat3.width > 935:
                                    self.Cplayer.boat3.width = 935
                                else:
                                    self.Cplayer.boat3.Fuel -= 1
                # Movement destroyer
                if self.DestroyerMovement == True:
                    if self.Cplayer.boat2.Fuel > 0:
                            if (self.width/37) + 20 > mouse_pos[0] > (self.width/37) and (self.height/2.59) + 20 > mouse_pos[1] > (self.height/2.59):
                                self.Cplayer.boat2.height -= 35.7
                                if self.Cplayer.boat2.height < 0:
                                    self.Cplayer.boat2.height = 0
                                else:
                                    self.Cplayer.boat2.Fuel -= 1
                            if (self.width/37) + 20 > mouse_pos[0] > (self.width/37) and (self.height/2.27) + 20 > mouse_pos[1] > (self.height/2.27):
                                self.Cplayer.boat2.height += 35.7
                                if self.Cplayer.boat2.height > 610:
                                    self.Cplayer.boat2.height = 610
                                else:
                                    self.Cplayer.boat2.Fuel -= 1
                            if (self.width/75) + 20 > mouse_pos[0] > (self.width/75) and (self.height/2.41) + 20 > mouse_pos[1] > (self.height/2.41):
                                self.Cplayer.boat2.width -= 35.7
                                if self.Cplayer.boat2.width < 275:
                                    self.Cplayer.boat2.width = 275
                                else:
                                    self.Cplayer.boat2.Fuel -= 1
                            if (self.width/23) + 20 > mouse_pos[0] > (self.width/23) and (self.height/2.41) + 20 > mouse_pos[1] > (self.height/2.41):
                                self.Cplayer.boat2.width += 35.7
                                if self.Cplayer.boat2.width > 955:
                                    self.Cplayer.boat2.width = 955
                                else:
                                    self.Cplayer.boat2.Fuel -= 1
                # Movement Battleship
                if self.BattleshipMovement == True:
                    if self.Cplayer.boat1.Fuel > 0:
                            if (self.width/37) + 20 > mouse_pos[0] > (self.width/37) and (self.height/1.400) + 20 > mouse_pos[1] > (self.height/1.400):
                                self.Cplayer.boat1.height -= 35.7
                                if self.Cplayer.boat1.height < 0:
                                    self.Cplayer.boat1.height = 0
                                else:
                                    self.Cplayer.boat1.Fuel -= 1
                            if (self.width/37) + 20 > mouse_pos[0] > (self.width/37) and (self.height/1.300) + 20 > mouse_pos[1] > (self.height/1.300):
                                self.Cplayer.boat1.height += 35.7
                                if self.Cplayer.boat1.height > 570:
                                    self.Cplayer.boat1.height = 570
                                else:
                                    self.Cplayer.boat1.Fuel -= 1
                            if (self.width/75) + 20 > mouse_pos[0] > (self.width/75) and (self.height/1.350) + 20 > mouse_pos[1] > (self.height/1.350):
                                self.Cplayer.boat1.width -= 35.7
                                if self.Cplayer.boat1.width < 275:
                                    self.Cplayer.boat1.width = 275
                                else:
                                    self.Cplayer.boat1.Fuel -= 1
                            if (self.width/23) + 20 > mouse_pos[0] > (self.width/23) and (self.height/1.350) + 20 > mouse_pos[1] > (self.height/1.350):
                                self.Cplayer.boat1.width += 35.7
                                if self.Cplayer.boat1.width > 955:
                                    self.Cplayer.boat1.width = 955
                                else:
                                    self.Cplayer.boat1.Fuel -= 1

    def blit_fuel(self, screen, Cplayer):
        if self.Cplayer.boat1.LifePoints > 0:
            self.Fuel_boat1 = self.font_FUEL.render(("Fuel: " + str(self.Cplayer.boat1.Fuel)), 1, (255,120,0))
            screen.blit(self.Fuel_boat1,((195) , (610)))
        if self.Cplayer.boat2.LifePoints > 0:
            self.Fuel_boat2 = self.font_FUEL.render(("Fuel: " + str(self.Cplayer.boat2.Fuel)), 1, (255,120,0))
            screen.blit(self.Fuel_boat2,((195) , (380))) 
        if self.Cplayer.boat3.LifePoints > 0:   
            self.Fuel_boat3 = self.font_FUEL.render(("Fuel: " + str(self.Cplayer.boat3.Fuel)), 1, (255,120,0))
            screen.blit(self.Fuel_boat3,((195) , (130)))

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
        self.currentturn = self.font2.render(('Turn: {}'.format(self.turn)), 1, (255, 120, 0))
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
        self.game = Game

class Boats:
    def __init__ (self, application, width, height, lifepoints, Fuel, Attrange, Deffrange, type, mode, AttPoints):
        self.application = application
        self.width = width
        self.height = height
        self.LifePoints = lifepoints
        self.Fuel = Fuel
        self.Attrange = Attrange
        self.Deffrange = Deffrange
        self.type = type
        self.Mode = mode
        self.AttPoints = AttPoints
        self.position = (self.width, self.height)

    def draw(self, screen):
        # Screen blit topview boats player 1
        if self.player1.boat1.LifePoints > 0:
            if self.player1.boat1.Mode == 'Att':
                screen.blit(self.Battleship, (self.application.game.player1.boat1.width, self.application.game.player1.boat1.height))
            elif self.player1.boat1.Mode == 'Deff':
                screen.blit(self.BattleshipR, (self.application.game.player1.boat1.width, self.application.game.player1.boat1.height))
        else:
            if self.player1.boat1.Mode == 'Att':
                screen.blit(self.BattleshipDES, (self.application.game.player1.boat1.width, self.application.game.player1.boat1.height))
            elif self.player1.boat1.Mode == 'Deff':
                screen.blit(self.BattleshipDESR, (self.application.game.player1.boat1.width, self.application.game.player1.boat1.height))

        if self.player1.boat2.LifePoints > 0:
            if self.player1.boat2.Mode == 'Att':
                screen.blit(self.Destroyer, (self.application.game.player1.boat2.width, self.application.game.player1.boat2.height))
            elif self.player1.boat2.Mode == 'Deff':
                screen.blit(self.DestroyerR, (self.application.game.player1.boat2.width, (self.application.game.player1.boat2.height - 10)))
        else:
            if self.player1.boat2.Mode == 'Att':
                screen.blit(self.DestroyerDES, (self.application.game.player1.boat2.width, self.application.game.player1.boat2.height))
            elif self.player1.boat2.Mode == 'Deff':
                screen.blit(self.DestroyerDESR, (self.application.game.player1.boat2.width, ( self.application.game.player1.boat2.height -10)))

        if self.player1.boat3.LifePoints > 0:
            if self.player1.boat3.Mode == 'Att':
                screen.blit(self.Gunboat, (self.application.game.player1.boat3.width, self.application.game.player1.boat3.height))
            elif self.player1.boat3.Mode == 'Deff':
                screen.blit(self.GunboatR, ((self.application.game.player1.boat3.width + 18), (self.application.game.player1.boat3.height -20 ))) 
        else:
            if self.player1.boat3.Mode == 'Att':
                screen.blit(self.GunboatDES, (self.application.game.player1.boat3.width, self.application.game.player1.boat3.height))
            elif self.player1.boat3.Mode == 'Deff':
                screen.blit(self.GunboatDESR, ((self.application.game.player1.boat3.width + 18), (self.application.game.player1.boat3.height -20)))       

        # Screen blit topview boats player 2
        if self.player2.boat1.LifePoints > 0:
            if self.player2.boat1.Mode == 'Att':
                screen.blit(self.Battleship2, (self.application.game.player2.boat1.width, self.application.game.player2.boat1.height))
            elif self.player2.boat1.Mode == 'Deff':
                screen.blit(self.Battleship2R, (self.application.game.player2.boat1.width, self.application.game.player2.boat1.height))
        else:
            if self.player2.boat1.Mode == 'Att':
                screen.blit(self.BattleshipDESP2, (self.application.game.player2.boat1.width, self.application.game.player2.boat1.height))
            elif self.player2.boat1.Mode == 'Deff':
                screen.blit(self.BattleshipDESP2R, (self.application.game.player2.boat1.width, self.application.game.player2.boat1.height))

        if self.player2.boat2.LifePoints > 0:
            if self.player2.boat2.Mode == 'Att':
                screen.blit(self.Destroyer2, (self.application.game.player2.boat2.width, self.application.game.player2.boat2.height))
            elif self.player2.boat2.Mode == 'Deff':
                screen.blit(self.Destroyer2R, ((self.application.game.player2.boat2.width + 7), self.application.game.player2.boat2.height))
        else:
            if self.player2.boat2.Mode == 'Att':
                screen.blit(self.DestroyerDESP2, (self.application.game.player2.boat2.width, self.application.game.player2.boat2.height))
            elif self.player2.boat2.Mode == 'Deff':
                screen.blit(self.DestroyerDES2R, (self.application.game.player2.boat2.width, self.application.game.player2.boat2.height))

        if self.player2.boat3.LifePoints > 0:
            if self.player2.boat3.Mode == 'Att':
                screen.blit(self.Gunboat2, (self.application.game.player2.boat3.width, self.application.game.player2.boat3.height))
            elif self.player2.boat3.Mode == 'Deff':
                screen.blit(self.Gunboat2R, ((self.application.game.player2.boat3.width + 20), (self.application.game.player2.boat3.height + 20)))
        else:
            if self.player2.boat3.Mode == 'Att':
                screen.blit(self.GunboatDESP2, (self.application.game.player2.boat3.width, self.application.game.player2.boat3.height))
            elif self.player2.boat3.Mode == 'Deff':
                screen.blit(self.GunboatDES2R, ((self.application.game.player2.boat3.width + 20), self.application.game.player2.boat3.height))

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
        self.get = self.application.database.get_score(screen)

class Tutorial:
    def __init__ (self, application, width, height):
        self.application = application
        self.Background = pygame.image.load("BackgroundA.jpg")
        self.Background = pygame.transform.scale(self.Background, (width, height))
        self.font = pygame.font.SysFont('Arial', 150)
        self.width = width
        self.height = height
        self.page = 1

        self.back_to_menu = Button(self.application, ("Back to menu"), (width/15), (height/1.25), 205, 40)
        self.back_to_game = Button(self.application, ("Back to game / start game"), (width/15), (height/1.4), 205, 40)
        self.previous = Button(self.application, ("Previous"), (width/15), (height/1.55), 205, 40)
        self.next = Button(self.application, ("Next"), (width/5), (height/1.55), 205, 40)
    
        self.P1 = pygame.image.load("Panel1.png")
        self.P1 = pygame.transform.scale(self.P1, (int(width/1.7), int(height/1.7)))

        self.P2 = pygame.image.load("Panel2.png")
        self.P2 = pygame.transform.scale(self.P2, (int(width/1.7), int(height/1.7)))

        self.P3 = pygame.image.load("Panel3.png")
        self.P3 = pygame.transform.scale(self.P3, (int(width/1.7), int(height/1.7)))

        self.P4 = pygame.image.load("Panel4.png")
        self.P4 = pygame.transform.scale(self.P4, (int(width/1.7), int(height/1.7)))

        self.P5 = pygame.image.load("Panel5.png")
        self.P5 = pygame.transform.scale(self.P5, (int(width/1.7), int(height/1.7)))
    
        self.P6 = pygame.image.load("Panel6.png")
        self.P6 = pygame.transform.scale(self.P6, (int(width/1.7), int(height/1.7)))

        self.P7 = pygame.image.load("Panel7.png")
        self.P7 = pygame.transform.scale(self.P7, (int(width/1.7), int(height/1.7)))

        self.P8 = pygame.image.load("Panel8.png")
        self.P8 = pygame.transform.scale(self.P8, (int(width/1.7), int(height/1.7)))

    def draw (self, screen):
        screen.blit(self.Background,(0,0))
        title_text = self.font.render("Tutorial", 1, (255,120,0))
        screen.blit(title_text,((self.width / 15) , (self.height / 9)))
        screen.blit(self.P2, (self.width/2.5, self.height/2.7))
        self.back_to_menu.mouse_action(screen)
        self.back_to_game.mouse_action(screen)
        self.previous.mouse_action(screen)
        self.next.mouse_action(screen)
        Application.back(self)

        if self.page == 1:
            screen.blit(self.P1, (self.width/2.5, self.height/2.7))
        elif self.page == 2:
            screen.blit(self.P2, (self.width/2.5, self.height/2.7))
        elif self.page == 3:
            screen.blit(self.P3, (self.width/2.5, self.height/2.7))
        elif self.page == 4:
            screen.blit(self.P4, (self.width/2.5, self.height/2.7))
        elif self.page == 5:
            screen.blit(self.P5, (self.width/2.5, self.height/2.7))
        elif self.page == 6:
            screen.blit(self.P6, (self.width/2.5, self.height/2.7))
        elif self.page == 7:
            screen.blit(self.P7, (self.width/2.5, self.height/2.7))
        elif self.page == 8:
            screen.blit(self.P8, (self.width/2.5, self.height/2.7))

class Victory:  
    def __init__ (self, application, width, height):
        self.application = application
        self.Background = pygame.image.load("VictoryBG.jpg")
        self.Background = pygame.transform.scale(self.Background, (width, height))
        self.font = pygame.font.SysFont('Arial', 150)
        self.font2 = pygame.font.SysFont('Arial',50)
        self.back_to_menu_button = Button(self.application, 'Back to menu', (width/15), (height/1.25), 170, 50)
        self.replay_button = Button(self.application, 'Replay', (width/15), (height/1.4), 170, 50)
        self.width = width
        self.height = height

    def draw (self, screen):
        screen.blit(self.Background,(0, 0))
        title_text = self.font.render("Victory", 1, (255,120,0))
        victory_text = self.font2.render("Congratulations {}. You have decimated the enemy.".format(str(self.application.game.Cplayer.name)), 1, (255,120,0))
        screen.blit(title_text,((self.width / 15) , (self.height / 9)))
        screen.blit(victory_text,((self.width / 15) , (self.height / 2.8)))
        self.back_to_menu_button.mouse_action(screen)
        self.replay_button.mouse_action(screen)

class Database:
    def __init__(self, application, width, height):
        self.application = application
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont('Arial', 50)

    def create(self):
        self.conn = psycopg2.connect("dbname=BattleportHighscore user=postgres password=080396-jeroen")
        self.cur = self.conn.cursor()
        self.cur.execute("DROP TABLE IF EXISTS Highscores;")
        self.cur.execute("CREATE TABLE Highscores (player_name varchar PRIMARY KEY, total_wins integer);")
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def update(self, Name): 
        self.conn = psycopg2.connect("dbname=BattleportHighscore user=postgres password=080396-jeroen")
        self.cur = self.conn.cursor()
        self.cur.execute("UPDATE highscores SET total_wins = total_wins + 1 WHERE player_name = '{}'".format(self.application.game.Cplayer.name))
        print(self.application.game.Cplayer.name)
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def get_score (self, screen):
        self.x = self.width
        self.y = self.height
        self.conn = psycopg2.connect("dbname=BattleportHighscore user=postgres password=080396-jeroen")
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM Highscores ORDER by total_wins DESC")
        self.HSveld = pygame.image.load("tekstveld1.png")
        self.HSveld = pygame.transform.scale(self.HSveld, (int(self.width/1.7), int(self.height/1.7)))
        screen.blit(self.HSveld, (self.width/2.5, self.height/2.7))
        
        for row in self.cur:
            ScoreDisplay = self.font.render(str(row), 0, (255,120,0))
            screen.blit(ScoreDisplay, ((self.x / 2),(self.y / 2)))
            self.y += 100

        self.conn.commit()
        self.cur.close()
        self.conn.close()

class Reset:
    def __init__(self, application):
        self.application = application
    def reset(self):
        self.application.game.player1.boat1.LifePoints = 5
        self.application.game.player1.boat2.LifePoints = 4
        self.application.game.player1.boat3.LifePoints = 3
        self.application.game.player2.boat1.LifePoints = 5
        self.application.game.player2.boat2.LifePoints = 4
        self.application.game.player2.boat3.LifePoints = 3
        self.application.game.player1.boat1.width = 453
        self.application.game.player1.boat2.width = 490     
        self.application.game.player1.boat3.width = 258
        self.application.game.player2.boat1.width = 458
        self.application.game.player2.boat2.width = 482     
        self.application.game.player2.boat3.width = 258
        self.application.game.player1.boat1.height = 571
        self.application.game.player1.boat2.height = 610
        self.application.game.player1.boat3.height = 645
        self.application.game.player2.boat1.height = 0
        self.application.game.player2.boat2.height = 0
        self.application.game.player2.boat3.height = 0
        self.application.game.GunboatMovement = False
        self.application.game.DestroyerMovement = False
        self.application.game.BattleshipMovement = False
        self.application.game.turn.turn = 1

def program():
    application = Application()
    application.application_loop()

program()