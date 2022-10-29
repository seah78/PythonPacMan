import pygame
import random

import utils.constants as constant


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, color, width, height):
        # Call the constructor of the parent class (Sprite) / Appelle le construteur de la classe parent (Sprite)
        pygame.sprite.Sprite.__init__(self)
        
        # Sets the background color as transparent / Définit la couleur d'arrière plan comme transparente
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        
class Ellipse(pygame.sprite.Sprite):
    def __init__(self, x, y, color, width, height):

        # Call the constructor of the parent class (Sprite) / Appelle le construteur de la classe parent (Sprite)
        pygame.sprite.Sprite.__init__(self)
        
        # Sets the background color as transparent / Définit la couleur d'arrière plan comme transparente
        self.image = pygame.Surface([width, height])
        self.image.fill(constant.BLACK)
        self.image.set_colorkey(constant.BLACK)
        
        # Draw the ellipse / Dessine l'ellipse
        pygame.draw.ellipse(self.image, color, [0 , 0, width, height])
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        
class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, change_x, change_y):
        
        # Call the constructor of the parent class (Sprite) / Appelle le construteur de la classe parent (Sprite)
        pygame.sprite.Sprite.__init__(self)
        
        # Defines the direction of the ghost / Définit la direction du fantôme
        self.change_x = change_x
        self.change_y = change_y
        
        # load the image / charge l'image
        self.image = pygame.image.load("files/ghost.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
    def update(self, horizontal_blocks, vertical_blocks):
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        
        if self.rect.right < 0:
            self.rect.left = constant.SCREEN_WIDTH
        elif self.rect.left > constant.SCREEN_WIDTH:
            self.rect.right = 0
            
        if self.rect.bottom < 0:
            self.rect.top = constant.SCREEN_HEIGHT
        elif self.rect.top > constant.SCREEN_HEIGHT:
            self.rect.bottom = 0
            
        if  self.rect.topleft in self.get_intersection_position():
            direction = random.choice(("left","right","up","down"))
            if direction == "left" and self.change_x == 0:
                self.change_x = -2
                self.change_y = 0
            elif direction == "right" and self.change_x == 0:
                self.change_x = 2
                self.change_y = 0
            elif direction == "up" and self.change_y == 0:
                self.change_x = 0
                self.change_y = -2
            elif direction == "down" and self.change_y == 0:
                self.change_x = 0
                self.change_y = 2
                
    def get_intersection_position(self):
        items = []
        for i,row in enumerate(enviroment()):
            items.extend((j*32, i*32) for j, item in enumerate(row) if item == 3)
        return items
  
    
# Definition of the playground / Définition du terrain de jeu
def enviroment():
    return ((0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,3,1),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,3,1),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,3,1),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,3,1),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0))
    

def draw_enviroment(screen):
    for i,row in enumerate(enviroment()):
        for j,item in enumerate(row):
            if item == 1:
                pygame.draw.line(screen, constant.BLUE , [j*32, i*32], [j*32+32,i*32], 3)
                pygame.draw.line(screen, constant.BLUE , [j*32, i*32+32], [j*32+32,i*32+32], 3)
            elif item == 2:
                pygame.draw.line(screen, constant.BLUE , [j*32, i*32], [j*32,i*32+32], 3)
                pygame.draw.line(screen, constant.BLUE , [j*32+32, i*32], [j*32+32,i*32+32], 3)
