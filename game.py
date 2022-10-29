#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from player import Player
from ghost import *
import tkinter
from tkinter import messagebox
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576

# game colors / couleurs du jeu
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)

class Game(object):
    def __init__(self):
        self.font = pygame.font.Font(None,40)
        self.about = False
        self.game_over = True
        # Create the variable for the score / Créer la variable pour le score
        self.score = 0
        # Create the font for displaying the score on the screen / Créer la police pour d'affichage du score à l'écran
        self.font = pygame.font.Font(None,35)
        # Create the menu of the game / Créer le menu du jeu
        self.menu = Menu(("Démarrer","A propos","Quitter"),font_color = WHITE,font_size=60)
        # Create the player / Créer le joueur
        self.player = Player(32,128,"files/player.png")
        # Create the blocks that will set the paths where the player can go / Crée les blocs qui définiront les chemins où le joueur pourra aller.
        self.horizontal_blocks = pygame.sprite.Group()
        self.vertical_blocks = pygame.sprite.Group()
        # Create a group for the dots on the screen / Créer un groupe de points sur l'écran
        self.dots_group = pygame.sprite.Group()
        # Set the enviroment / Définit l'environnement
        for i,row in enumerate(enviroment()):
            for j,item in enumerate(row):
                if item == 1:
                    self.horizontal_blocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
                elif item == 2:
                    self.vertical_blocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
        # Create the ghosts / Création des fantômes
        self.enemies = pygame.sprite.Group()
        self.enemies.add(Ghost(288,96,0,2))
        self.enemies.add(Ghost(288,320,0,-2))
        self.enemies.add(Ghost(544,128,0,2))
        self.enemies.add(Ghost(32,224,0,2))
        self.enemies.add(Ghost(160,64,2,0))
        self.enemies.add(Ghost(448,64,-2,0))
        self.enemies.add(Ghost(640,448,2,0))
        self.enemies.add(Ghost(448,320,2,0))
        # Add the dots inside the game / Ajoutez les points dans le terrain de jeu
        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item != 0:
                    self.dots_group.add(Ellipse(j*32+12,i*32+12,WHITE,8,8))

        # Load the sound effects / Charge les effets sonores
        self.pacman_sound = pygame.mixer.Sound("files/pacman_sound.ogg")
        self.game_over_sound = pygame.mixer.Sound("files/game_over_sound.ogg")


    def process_events(self):
        for event in pygame.event.get(): # Detection of player's actions / Détection des actions du joueur
            if event.type == pygame.QUIT: # If user clicked close / Si l'utilisateur a cliqué sur quitter, propose le choix entre DEMARRER, A PROPOS, QUITTER
                return True
            self.menu.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.game_over and not self.about:
                        if self.menu.state == 0:
                            # ---- DEMARRER ------
                            # User clicked start / L'utilisateur a cliqué sur démarrer
                            self.__init__()
                            self.game_over = False
                        elif self.menu.state == 1:
                            # --- A PROPOS ------
                            # User clicked about / L'utilisateur a cliqué sur à propos
                            self.about = True
                        elif self.menu.state == 2:
                            # --- Quitter -------
                            # User clicked exit / L'utilisateur a cliqué sur quitter
                            return True

                elif event.key == pygame.K_RIGHT:
                    self.player.move_right()

                elif event.key == pygame.K_LEFT:
                    self.player.move_left()

                elif event.key == pygame.K_UP:
                    self.player.move_up()

                elif event.key == pygame.K_DOWN:
                    self.player.move_down()
                
                elif event.key == pygame.K_ESCAPE:
                    self.game_over = True
                    self.about = False

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.stop_move_right()
                elif event.key == pygame.K_LEFT:
                    self.player.stop_move_left()
                elif event.key == pygame.K_UP:
                    self.player.stop_move_up()
                elif event.key == pygame.K_DOWN:
                    self.player.stop_move_down()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.player.explosion = True
                    
        return False

    def run_logic(self):
        if not self.game_over:
            self.player.update(self.horizontal_blocks,self.vertical_blocks)
            block_hit_list = pygame.sprite.spritecollide(self.player,self.dots_group,True)
            # When the block_hit_list contains one sprite that means that player hit a dot / Lorsque la block_hit_list contient un sprite, cela signifie que le joueur a touché un point.
            if len(block_hit_list) > 0:
                # Triggering the sound effect / Déclenchement de l'effet sonore
                self.pacman_sound.play()
                self.score += 1
            block_hit_list = pygame.sprite.spritecollide(self.player,self.enemies,True)
            if len(block_hit_list) > 0:
                self.player.explosion = True
                self.game_over_sound.play()
            self.game_over = self.player.game_over
            self.enemies.update(self.horizontal_blocks,self.vertical_blocks)
           # tkMessageBox.showinfo("GAME OVER!","Final Score = "+(str)(GAME.score))    

    def display_frame(self,screen):
        # First, clear the screen to white. Don't put other drawing commands / Tout d'abord, effacez l'écran en blanc. Ne mettez pas d'autres commandes de dessin
        screen.fill(BLACK)
        # --- Drawing code should go here / Le code de dessin vient ici
        if self.game_over:
            if self.about:
                self.display_message(screen,"It is an arcade Game / C'est un eu d'arcade")
                #"a maze containing various dots,\n"
                #known as Pac-Dots, and four ghosts.\n"
                #"The four ghosts roam the maze, trying to kill Pac-Man.\n"
                #"If any of the ghosts hit Pac-Man, he loses a life;\n"
                #"the game is over.\n")
                
                #"un labyrinthe contenant plusieurs points,\n"
                #connus sous le nom de Pac-Dots, et quatre fantômes.\n"
                #"Les quatre fantômes errent dans le labyrinthe, essayant de tuer Pac-Man.\n"
                #"Si l'un des fantômes touche Pac-Man, il perd une vie ;\n"
                #"le jeu est terminé.\n")
                
            else:
                self.menu.display_frame(screen)
        else:
            # --- Drawing of the playground / Dessin du terrain de jeu ---
            self.horizontal_blocks.draw(screen)
            self.vertical_blocks.draw(screen)
            draw_enviroment(screen)
            self.dots_group.draw(screen)
            self.enemies.draw(screen)
            screen.blit(self.player.image,self.player.rect)
            #text=self.font.render("Score: "+(str)(self.score), 1,self.RED)
            #screen.blit(text, (30, 650))
            # Render the text for the score / Rendu du texte pour le score
            text = self.font.render("Score: " + str(self.score),True,GREEN)
            # Put the text on the screen / Met le texte sur l'écran
            screen.blit(text,[120,20])
            
        # --- Updates the screen with what we have drawn / Met à jour l'écran avec ce que nous avons dessiné
        pygame.display.flip()

    def display_message(self,screen,message,color=(255,0,0)):
        label = self.font.render(message,True,color)
        # Get the width and height of the label / Obtenir la largeur et la hauteur de l'étiquette
        width = label.get_width()
        height = label.get_height()
        # Determine the position of the label / Détermine la position de l'étiquette
        posX = (SCREEN_WIDTH /2) - (width /2)
        posY = (SCREEN_HEIGHT /2) - (height /2)
        # Draw the label onto the screen / Dessine l'étiquette sur l'écran
        screen.blit(label,(posX,posY))


class Menu(object):
    state = 0
    def __init__(self,items,font_color=(0,0,0),select_color=(255,0,0),ttf_font=None,font_size=25):
        self.font_color = font_color
        self.select_color = select_color
        self.items = items
        self.font = pygame.font.Font(ttf_font,font_size)
        
    def display_frame(self,screen):
        for index, item in enumerate(self.items):
            if self.state == index:
                label = self.font.render(item,True,self.select_color)
            else:
                label = self.font.render(item,True,self.font_color)
            
            width = label.get_width()
            height = label.get_height()
            
            posX = (SCREEN_WIDTH /2) - (width /2)
            # t_h: total height of text block
            t_h = len(self.items) * height
            posY = (SCREEN_HEIGHT /2) - (t_h /2) + (index * height)
            
            screen.blit(label,(posX,posY))
        
    def event_handler(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.state > 0:
                    self.state -= 1
            elif event.key == pygame.K_DOWN:
                if self.state < len(self.items) -1:
                    self.state += 1
