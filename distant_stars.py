import pygame
import math
import random

class Distant_Stars(pygame.sprite.Group):
    
    #class constants    
    STARS_SMALL = 50
    STARS_MED = 20
    STARS_LARGE = 5
    
    #loading images
    SMALL_IMAGE = pygame.image.load('Images/star_small.png')
    MED_IMAGE = pygame.image.load('Images/star_med.png')
    LARGE_IMAGE = pygame.image.load('Images/star_large.png')

    def __init__(self, game):
        
        pygame.sprite.Group.__init__(self)
        
        '''random generation of stars in the background'''
        
        for i in range(Distant_Stars.STARS_SMALL):
            x = random.randint(0, game.screen_width)
            y = random.randint(0, game.screen_height)
            position = (x, y)
            star = Star(game, position, Distant_Stars.SMALL_IMAGE)
            self.add(star)
        
        for i in range(Distant_Stars.STARS_MED):
            x = random.randint(0, game.screen_width)
            y = random.randint(0, game.screen_height)
            position = (x, y)
            star = Star(game, position, Distant_Stars.MED_IMAGE)
            self.add(star)

        for i in range(Distant_Stars.STARS_LARGE):
            x = random.randint(0, game.screen_width)
            y = random.randint(0, game.screen_height)
            position = (x, y)
            star = Star(game, position, Distant_Stars.LARGE_IMAGE)
            self.add(star)



class Star(pygame.sprite.Sprite):
    
    def __init__(self, game, position, img):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.game = game
        self.position = position
        self.screen = game.screen
        self.image = img
        self.image.convert()
        self.rect = self.image.get_rect()


    def move_gradient(self):

        '''getting the change in x and y coordinates according to the rotation of spacecraft'''
        
        move_y = math.cos(math.radians(self.game.spacecraft.angle+ 180))
        move_x = math.sin(math.radians(self.game.spacecraft.angle + 180))

        x = self.game.spacecraft.speed * move_x
        y = self.game.spacecraft.speed * move_y
        
        return(-x, -y)

    def move(self):

        '''Moves the background according to the rotation of spacecraft'''
        
        self.pos = self.move_gradient()

        self.position = (self.position[0] + self.pos[0], self.position[1]+ self.pos[1] )
        
        #if stars gets outside the screen, it is generated again
        if self.position[1] > self.game.screen_height:
            self.position = (random.randint(0, self.game.screen_width), 0)

        if self.position[0] > self.game.screen_width:
            self.position = (0, random.randint(0, self.game.screen_height))

        if self.position[1] < 0:
            self.position = (random.randint(0, self.game.screen_width), self.game.screen_height)

        if self.position[0] < 0:
            self.position = (self.game.screen_width, random.randint(0, self.game.screen_height))


    def update(self):
        
        '''updates the position of stars'''
        self.move()
        self.screen.blit(self.image, self.position)
