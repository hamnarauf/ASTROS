import pygame
import random
import math
from collisions import Collision
from pygame import mixer
pygame.mixer.init()

#loading sound
hurdle_sound = mixer.Sound('Music/explosion.mp3')
booster_sound = mixer.Sound('Music/booster.mp3')

#parent class
class Flying_Object(pygame.sprite.Sprite):
    
    count = 1

    def __init__(self):

        super().__init__()
        self.img.convert()
        self.rect = self.img.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.screen_rect = self.game.screen.get_rect()
        self.screen_width = self.game.screen_width              
        self.screen_height = self.game.screen_height
        
        self.initial_position()
        Flying_Object.count += 1
        self.game.fl_objs.add(self)


    def initial_position(self):
        
        '''Assigns x and y coordinates randomly to each object'''
        
        sides = [1,2,3,4,5,6,7,8]
        self.side = random.choice(sides)

        if self.side == 1:
            self.x = random.randrange(0,self.screen_rect.width/2)
            self.y = -self.height
        
        elif self.side == 2:
            self.x =random.randrange(self.screen_rect.width/2,self.screen_rect.width)
            self.y = -self.height
                
        elif self.side == 3:
            self.x = self.screen_rect.width + self.width
            self.y = random.randrange(0, self.screen_rect.height/2)

        elif self.side == 4:
            self.x = self.screen_rect.width + self.width
            self.y = random.randrange(self.screen_rect.height/2, self.screen_rect.height)
               
        elif self.side == 5:
            self.x =random.randrange(self.screen_rect.width/2,self.screen_rect.width)
            self.y = self.screen_rect.height + self.height
                
        elif self.side == 6:
            self.x = random.randrange(0, self.screen_rect.width/2)
            self.y = self.screen_rect.height + self.height

        elif self.side == 7:
            self.x = -self.width
            self.y = random.randrange(self.screen_rect.height/2, self.screen_rect.height)

        elif self.side == 8:
            self.x = -self.width
            self.y = random.randrange(0, self.screen_rect.height/2)


    def move(self, speed = 0.5):
        
        ''''Moves the images according to the side'''
        if self.side == 1 or self.side == 8:
            self.x += speed
            self.y += speed
        elif self.side == 2 or self.side == 3:
            self.x -= speed
            self.y += speed
        elif self.side == 4 or self.side == 5:
            self.x -= speed
            self.y -= speed
        elif self.side == 6 or self.side == 7:
            self.x += speed
            self.y -= speed
    

    def destroy(self):                 
        
        '''Destroying object once it gets out of the screen'''
        
        if (self.side == 1 or self.side == 8) and (self.x > self.screen_width + self.width or self.y > self.screen_height + self.height ):
            self.game.fl_objs.remove(self)
            del self
    
        elif (self.side == 2 or self.side == 3) and (self.x < -self.screen_width - self.width or self.y > self.screen_height + self.height):
            self.game.fl_objs.remove(self)
            del self
            
        elif (self.side == 4 or self.side == 5) and (self.x < -self.screen_width - self.width or self.y < -self.screen_height - self.height):
            self.game.fl_objs.remove(self)
            del self
            
        elif (self.side == 6 or self.side == 7) and (self.x > self.screen_width + self.width or self.y < -self.screen_height - self.height):
            self.game.fl_objs.remove(self)
            del self
            

    def update(self):
        
        '''Updates the status of flying objects'''
        if self.game.fl_objs.frost_ball == False:
            self.move()
        self.destroy()
        self.rect = self.img.get_rect(topleft = (self.x, self.y))
        self.game.screen.blit(self.img , self.rect)
        self.mask = pygame.mask.from_surface(self.img)
        

#Child classes
class Small_Asteroid(Flying_Object):

    IMAGE = pygame.image.load("Images/smaller asteroid.png")

    def __init__(self, game):

        self.img = Small_Asteroid.IMAGE
        self.game = game

        super().__init__()

    #collision methods
    def collide_spacecraft(self):
        Collision.spacecraft_small_asteroid(self.game)

    def collide_bullet(self):                               
        Collision.bullet_small_asteroid(self.game)


class Large_Asteroid(Flying_Object):
    
    IMAGE = pygame.image.load("Images/larger asteroid.png")

    def __init__(self, game):
        self.img = Large_Asteroid.IMAGE
        self.game = game
        self.times_collision = 0
        
        super().__init__()
    
    #collision methods
    def collide_spacecraft(self):
        Collision.spacecraft_large_asteroid(self.game)

    def collide_bullet(self):
        Collision.bullet_large_asteroid(self.game)


class Comet1(Flying_Object):
    
    IMAGE = pygame.image.load("Images/comet1.png")

    def __init__(self, game):
        self.img = Comet1.IMAGE
        self.game = game
        
        super().__init__()
    
    #collision methods
    def collide_spacecraft(self):
        Collision.spacecraft_comet1(self.game)

    def collide_bullet(self):
        Collision.bullet_comet1(self.game)


class Comet2(Flying_Object):

    IMAGE = pygame.image.load("Images/comet2.png")
    
    def __init__(self, game):
        self.img = Comet2.IMAGE
        self.game = game

        super().__init__()
    
    #collision methods
    def collide_spacecraft(self):
        Collision.spacecraft_comet2(self.game) 

    def collide_bullet(self):
        Collision.bullet_comet2(self.game)


class Frost_Ball(Flying_Object):

    IMAGE = pygame.image.load("Images/frost ball.png")
    
    def __init__(self, game):
        self.img = Frost_Ball.IMAGE
        self.game = game
        
        super().__init__()
    
    #collision methods
    def collide_spacecraft(self):
        Collision.spacecraft_frost_ball(self.game)

    def collide_bullet(self):
        Collision.bullet_frost_ball(self.game)


class Health_Booster(Flying_Object):

    IMAGE = pygame.image.load("Images/health booster.png")
    
    def __init__(self, game):
        self.img = Health_Booster.IMAGE
        self.game = game
        
        super().__init__()
        
    #collision methods
    def collide_spacecraft(self):
        Collision.spacecraft_health_booster(self.game)

    def collide_bullet(self):
        Collision.bullet_health_booster(self.game)



class Black_Holes(Flying_Object):
    
    IMAGE = pygame.image.load("Images/blackhole.png")
    
    def __init__(self, game):
        
        self.game = game
        self.img = Black_Holes.IMAGE
        self.blackholeX, self.blackholeY = self.img.get_size()
        self.angle = 0
        
        super().__init__()


    def initial_position(self):
        
        self.x = random.randrange(-self.blackholeX, self.screen_width - self.blackholeX)
        self.y = random.randrange(-self.blackholeY, self.screen_height - self.blackholeY)

        #making sure that black hole is not generated in the close vacanity of spacecraft 
        excluded_x = range(int(self.screen_width/2 - self.game.spacecraft.rect.width/2), int(self.screen_width/2 + self.game.spacecraft.rect.width/2))
        excluded_y = range(int(self.screen_height/2 - self.game.spacecraft.rect.height/2), int(self.screen_height/2 + self.game.spacecraft.rect.height/2))

        while self.x in (excluded_x) and self.y in (excluded_y):
            self.x = random.randrange(-self.blackholeX, self.screen_width - self.blackholeX)
            self.y = random.randrange(-self.blackholeY, self.screen_height - self.blackholeY)

    
    def rotate(self):
        
        '''Rotates the black hole'''
        
        self.rotated_img = pygame.transform.rotozoom(self.img, self.angle, 1)
        self.rect = self.rotated_img.get_rect(center = (self.x, self.y))
        self.game.screen.blit(self.rotated_img , self.rect)
        self.mask = pygame.mask.from_surface(self.img)
        
        self.angle -= .75
        if self.angle <= -360:
            self.angle = 0
        
    def angle_position(self):
        
        '''Change in position of black hole according to the spaecraft's movement'''

        cosine = math.cos(math.radians(self.game.spacecraft.angle + 180)) 
        sine = math.sin(math.radians(self.game.spacecraft.angle + 180))

        move_x = self.game.spacecraft.speed * sine
        move_y = self.game.spacecraft.speed * cosine

        return (-move_x, -move_y)
    

    def move(self):
        '''move the black hole accorgint to spacecraft's movement'''
        
        self.position = self.angle_position()
        self.x, self.y = (self.x + self.position[0], self.y + self.position[1] )

        #destroying the black hole once it gets out of the screen
        if self.y > self.game.screen_height + self.blackholeY :
            self.game.fl_objs.remove(self)
            del self
            
        elif self.x > self.game.screen_width + self.blackholeX:
            self.game.fl_objs.remove(self)
            del self
            
        elif self.y < -self.blackholeY:
            self.game.fl_objs.remove(self)
            del self

        elif self.x < -self.blackholeX:
            self.game.fl_objs.remove(self)
            del self

    def update(self):
        self.rotate()
        self.move()
        
    #collide methods of black hole
    def collide_spacecraft(self):
        Collision.spacecraft_black_hole(self.game)

    def collide_bullet(self):
        Collision.bullet_black_hole(self.game)


class Flying_Object_Collection(pygame.sprite.Group):

    def __init__(self, game):   
        
        pygame.sprite.Group.__init__(self)

        self.HURDLES = ['Small_Asteroid', 'Large_Asteroid', 'Comet1', 'Comet2']
        self.BOOSTERS = ['Health_Booster',  'Frost_Ball']
        self.game = game
        self.frost_ball = False       

    #random selection of flying objects
        
    def create_flying_object(self, count):

        if count % 8 == 0:
            booster = random.choice(self.BOOSTERS)
            if booster == 'Health_Booster':
                return Health_Booster(self.game)
            
            else:
                return Frost_Ball(self.game)


        if count % 2 == 0:
            return Black_Holes(self.game)
            
        else:
            hurdle = random.choice(self.HURDLES)
            
            if hurdle == 'Small_Asteroid':
                return Small_Asteroid(self.game)

            elif hurdle == 'Large_Asteroid':
                return Large_Asteroid(self.game)

            elif hurdle == 'Comet1':
                return Comet1(self.game)

            elif hurdle == 'Comet2':
                return Comet2(self.game)


    def update(self):

        super().update()
        
        #checking collisions between spacecraft and flying objects
        
        if pygame.sprite.spritecollide(self.game.spacecraft, self, False, pygame.sprite.collide_rect):    
            
            object_colliding_spacecraft = pygame.sprite.spritecollide(self.game.spacecraft, self, True, pygame.sprite.collide_mask)     
            for element in object_colliding_spacecraft:
                element.collide_spacecraft()                        #calling collide method
                self.game.fl_objs.remove(element)
                del element                                         #deleting obj from the memory


    def collide(self, bullet):
        
        '''Checking collisions between bullet and flying objects'''
        
        if pygame.sprite.spritecollide(bullet, self, False):
            objects_colliding_bullet = pygame.sprite.spritecollide(bullet, self, False, pygame.sprite.collide_mask)   
            
            for element in objects_colliding_bullet:
                if isinstance(element, Large_Asteroid) and (element.times_collision < 3):       
                    element.times_collision += 1
                
               
                elif isinstance(element, Black_Holes):
                    del bullet

                else:
                    element.collide_bullet() 
                    self.game.fl_objs.remove(element)
                    del element
                    del bullet
                    hurdle_sound.play()
                        

