import pygame
from pygame import mixer

from bullet import Bullet, Bullet_Group
from flying_objects import Flying_Object_Collection


class Spacecraft(pygame.sprite.Sprite):
    
    #spacecraft constants
    SPEED_MAX = 3.0
    SPEED_MIN = 0.1
    SPEED_AVG = (SPEED_MAX + SPEED_MIN)/2
    
    #health constants
    HEALTH_MAX = 3
    HEALTH_MIN = 1
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

 
    def __init__(self, game):

        pygame.sprite.Sprite.__init__(self)
        
        self.game = game
        self.screen = self.game.screen
        self.screen_rect = self.screen.get_rect()
        
        self.image = pygame.image.load('Images/hub_small.png')
        self.image.convert()
        self.rotated_image = self.image
            
        self.rect = self.rotated_image.get_rect(center = self.screen_rect.center)
        self.rect.center = self.screen_rect.center
        self.length = self.rect.height


        self.rotate_right = False
        self.rotate_left = False
        self.angle = 0


        self.speed_up = False
        self.slow_down = False
        self.speed = Spacecraft.SPEED_AVG


        self.x_red_bar = self.screen.get_width() - 30
        self.y_red_bar = 20
        self.x_green_bar = self.screen.get_width() - 30
        self.y_green_bar = 20

        self.length_green_bar = 200

        self.reduction_factor = 1
        self.health = 4


        self.bullet_grp = Bullet_Group()
        self.muzzle_pos = self.image.get_rect(center = self.screen_rect.center).midtop
        self.firing = False


    def update(self):
        
        '''updates the position of spacecraft acoording to the key event by the user'''
        
        if self.rotate_right:
            self.angle -= 1
            if self.angle == -360:
                self.angle = 0
            self.rotated_image = pygame.transform.rotozoom(self.image, self.angle, 1)
            self.rect = self.rotated_image.get_rect()
            self.rect.center = self.screen_rect.center
            
        if self.rotate_left:
            self.angle += 1
            if self.angle == 360:
                self.angle = 0
            self.rotated_image = pygame.transform.rotozoom(self.image, self.angle, 1)
            self.rect = self.rotated_image.get_rect()
            self.rect.center = self.screen_rect.center
            
        if self.speed_up:
            if self.speed < Spacecraft.SPEED_MAX:
                self.speed += 0.0050

        if self.slow_down:
            if self.speed > Spacecraft.SPEED_MIN:
                self.speed -= 0.0050

        if self.firing:
            bullet = Bullet(self, self.game)                #calling Bullet class
            self.bullet_grp.add(bullet)

        self.screen.blit(self.rotated_image, self.rect)
        self.mask = pygame.mask.from_surface(self.rotated_image)



        self.bullet_grp.update()
        self.display_health_bar()

        
        for bullet_elm in self.bullet_grp:
            self.bullet_grp.remove(bullet_elm)          
            self.game.fl_objs.collide(bullet_elm)           #calling collision method from fl_objs
            self.bullet_grp.add(bullet_elm)


    def display_health_bar(self):
        
        '''displaying health bar of spacecraft'''
        pygame.draw.rect(self.screen, Spacecraft.RED, (self.x_red_bar, self.y_red_bar, 10, 200))
        pygame.draw.rect(self.screen, Spacecraft.GREEN, (self.x_green_bar, self.y_green_bar, 10, self.length_green_bar))


    def reduce_health(self, destruction_level):
        
        '''method reduces the health of the spacecraft and result is shown by decrease in the lenght of green part of health bar'''
        
        if self.health >= Spacecraft.HEALTH_MIN:
            self.health -= destruction_level
            
            self.length_green_bar = 50 * self.health
            self.y_green_bar = self.y_green_bar + destruction_level * 50

            if self.health < Spacecraft.HEALTH_MIN:
                self.game.game_over()
            
        
    def increase_health(self):

        '''method increases the health of the spacecraft and result is shown by increase in the lenght of green part of health bar'''
        
        if self.health <= Spacecraft.HEALTH_MAX:
            self.health += 1
            self.length_green_bar = 50 * self.health
            self.y_green_bar = self.y_green_bar - 50
