import pygame
from pygame import mixer
import math

#loading sound
bullet_sound = mixer.Sound('Music/laser.mp3')

class Bullet(pygame.sprite.Sprite):

    IMAGE = pygame.image.load('Images/ammo.png')

    def __init__(self, spacecraft, game):

        super().__init__()
        bullet_sound.play()

        self.game = game
        self.spacecraft = spacecraft

        self.img = Bullet.IMAGE
        self.rect = self.img.get_rect(midbottom = self.spacecraft.muzzle_pos)
 
        self.angle = self.spacecraft.angle


        #x and y coordinates of for bullet
        self.y = self.rect.y + self.spacecraft.length/2 - (self.spacecraft.length/2)*math.cos(math.radians(self.angle))
        self.x = self.rect.x - (self.spacecraft.length/2)*math.sin(math.radians(self.angle))
        self.rotated_image = pygame.transform.rotozoom(self.img, self.angle, 1)

        self.initial_pos = (self.x, self.y)
        self.speed = self.spacecraft.speed + 2


    def move_gradient(self):
        
        '''movement according to the rotation of spacecraft'''
        
        move_y = math.cos(math.radians(self.angle))
        move_x = math.sin(math.radians(self.angle))

        x = self.speed * move_x
        y = self.speed * move_y
        return(-x, -y)

    
    def move(self):

        self.pos = self.move_gradient()
        self.initial_pos = (self.initial_pos[0] + self.pos[0], self.initial_pos[1]+ self.pos[1] )
        

    def remove(self):
        
        '''deleting the bullet'''
        if not(self.game.screen.get_rect().collidepoint(self.initial_pos)):
            self.spacecraft.bullet_grp.remove(self)
            del self


    def update(self):
        
        '''úpdates the position of bullet'''
        self.game.screen.blit(self.rotated_image, self.initial_pos)
        self.rect = self.rotated_image.get_rect(topleft = self.initial_pos)
        self.mask = pygame.mask.from_surface(self.rotated_image)
        self.move()
        self.remove()



class Bullet_Group(pygame.sprite.Group):
    
    def __init__(self):
        
        super().__init__()
        

