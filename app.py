#ASTROS APPLICATION
import sys
import pygame
from pygame import mixer
import threading

from flying_objects import Flying_Object_Collection, Flying_Object
from distant_stars import Distant_Stars
from spacecraft import Spacecraft
from collisions import Collision



class Astros:
    def __init__(self):
        
        #loading music
        mixer.music.load('Music/bg.mp3')
        mixer.music.play(-1)

        #setting background and display
        self.background_colour = (0, 0, 0)
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

        #getting screen width and height
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        
        #calling classes
        self.spacecraft = Spacecraft(self)
        self.bg_stars = Distant_Stars(self)
        self.fl_objs = Flying_Object_Collection(self)

        self.score = 0
        self.level = 1
        self.spawn_freq_factor = 4500
        
        self.score_font = pygame.font.SysFont("Calibri", 30)

        #making event for trigering the time for respawn
        self.SPAWN = pygame.USEREVENT        
        pygame.time.set_timer(self.SPAWN, self.spawn_freq_factor)

        #setting FPS to make sure smooth movement of game
        self.FPS = 360
        self.clock = pygame.time.Clock()
    

    def _fire_bullet(self):
        
        self.spacecraft.firing = True
        pygame.time.wait(500)
        self.spacecraft.firing = False

    def _check_key_down_events(self, event):

        '''This method deals with the key down event'''
        
        if event.key == pygame.K_RIGHT:
            self.spacecraft.rotate_right = True

        if event.key == pygame.K_LEFT:
            self.spacecraft.rotate_left = True

        if event.key == pygame.K_UP:
            self.spacecraft.speed_up = True

        if event.key == pygame.K_DOWN:
            self.spacecraft.slow_down = True
                
        if event.key == pygame.K_ESCAPE:
            self.destroy()
            
        
        if event.key == pygame.K_SPACE:

            bullet_thread = threading.Thread(target = self._fire_bullet)
            bullet_thread.start()

    def _check_key_up_events(self, event):

        '''This method deals with all key up events'''
        
        if event.key == pygame.K_RIGHT:
            self.spacecraft.rotate_right = False

        if event.key == pygame.K_LEFT:
            self.spacecraft.rotate_left = False
        
        if event.key == pygame.K_UP:
            self.spacecraft.speed_up = False

        if event.key == pygame.K_DOWN:
            self.spacecraft.slow_down = False

        if event.key == pygame.K_SPACE:
            self.spacecraft.firing = False

    def _check_events(self):
        
        '''checking all events'''
        for event in pygame.event.get():

            #keydown
            if event.type == pygame.KEYDOWN:
                self._check_key_down_events(event)

            #keyup
            elif event.type == pygame.KEYUP:
                self._check_key_up_events(event)

            #spawn    
            elif event.type == self.SPAWN:

                if self.fl_objs.frost_ball == False:
                    self.fl_objs.create_flying_object(Flying_Object.count)

            #booster's active time
            if self.fl_objs.frost_ball and pygame.time.get_ticks()- self.frost_ball_timer > 7000:
                self.fl_objs.frost_ball = False
  

    def update_score(self):
        
        '''updates the score on the screen'''
        
        self.score_txt = self.score_font.render('Score: ' + str(self.score), True, (255, 255, 255))
        self.x_score = self.screen.get_rect().x + self.score_txt.get_rect().right/8
        self.y_score = self.screen.get_rect().y + self.score_txt.get_rect().bottom/2
        self.pos_score = (self.x_score, self.y_score)

        self.screen.blit(self.score_txt, self.pos_score)


    def update_level(self):
        '''updates the level'''
        
        if self.score >= self.level * 20:                   #condition for level up
            level_music = mixer.Sound('Music/levelup.mp3')
            level_music.play()

            self.level += 1

            if self.level <= 4:
                level_up_img = pygame.image.load('Images/Level_Up.jpg')
                self.screen.blit(pygame.transform.smoothscale(level_up_img, self.screen.get_size()), (0,0))
                pygame.display.flip()

                pygame.time.delay(2500)

                
                self.spawn_freq_factor -= 1100

                self.SPAWN = pygame.USEREVENT        
                pygame.time.set_timer(self.SPAWN, self.spawn_freq_factor)

            else:                                   #if the user survived till the end of 4th level, he is declared as a winner
                winner_img = pygame.image.load('Images/Winner.jpg')
                self.screen.blit(pygame.transform.smoothscale(winner_img, self.screen.get_size()), (0,0))
                pygame.display.flip()

                pygame.time.delay(2500)
                self.running = False


    def game_over(self):
        
        '''method for game over'''
        
        self.game_over_font = pygame.font.SysFont("Arial", 100 , True)
        self.game_over_txt = self.game_over_font.render('Game Over!', True, (255, 0, 0))

        self.x_game_over = self.screen.get_rect().centerx - self.game_over_txt.get_rect().width/2
        self.y_game_over = self.screen.get_rect().centery - self.game_over_txt.get_rect().height/2
        self.pos_game_over = (self.x_game_over, self.y_game_over)

        self.screen.blit(self.game_over_txt, (self.pos_game_over))
        pygame.display.flip()

        pygame.time.delay(2000)
        self.destroy()

   
    def destroy(self):
        
        mixer.music.stop()
        self.running = False
    

    def _update_screen(self):

        '''úpdates all the elements of the game'''
        self.screen.fill(self.background_colour)

        self.bg_stars.update()
        self.fl_objs.update()
        self.spacecraft.update()
        
        self.update_score()
        self.update_level()

        pygame.display.flip()
            

    def run_game(self):
        
        ''''main game loop'''
        self.running = True
        while self.running:

            self._check_events()
            self._update_screen()
            self.clock.tick(self.FPS)



class Splash_Screen:
    
    def __init__(self):
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.splash_img = pygame.image.load('Images/Splash Window.png')

        mixer.music.load('Music/menu.mp3')
        mixer.music.play(-1)
        self.display_splash()

    def display_splash(self):
        
        while pygame.time.get_ticks() < 2500:           #splash screen will be displayed for a few seconds in the start
            self.screen.blit(pygame.transform.smoothscale(self.splash_img, self.screen.get_size()), (0,0))
            pygame.display.flip()



class Main_Menu:

    def __init__(self):

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.main_menu_img = pygame.image.load('Images/Background.jpg')
        self.menu_font = pygame.font.SysFont('Calibri', 50, True)
        self.get_menu_buttons()
        self.main_menu()


    def get_menu_buttons(self):
        
        '''displays all the main menu buttons and gets a rectangle around it'''
        
        self.play_txt = self.menu_font.render('Play', True, (255, 255, 255))
        self.inst_txt = self.menu_font.render('Instructions', True, (255, 255, 255))
        self.credits_txt = self.menu_font.render('Credits', True, (255, 255, 255))
        self.exit_txt = self.menu_font.render('Exit', True, (255, 255, 255))
        self.back_txt = self.menu_font.render('Back', True, (255,255,255))

        self.x_play = (self.screen_width/2) - (self.play_txt.get_width() / 2)
        self.y_play = self.screen_height /3.2
        self.pos_play = (self.x_play, self.y_play)

        self.x_inst = (self.screen_width/2) - (self.inst_txt.get_width() / 2)
        self.y_inst = self.y_play + 1.5 * (self.play_txt.get_height())
        self.pos_inst = (self.x_inst, self.y_inst)

        self.x_credits = (self.screen_width/2) - (self.credits_txt.get_width() / 2)
        self.y_credits = self.y_inst + 1.5 * (self.inst_txt.get_height())
        self.pos_credits = (self.x_credits, self.y_credits)
        
        self.x_exit = (self.screen_width/2) - (self.exit_txt.get_width() / 2)
        self.y_exit = self.y_credits + 1.5 * (self.credits_txt.get_height())
        self.pos_exit = (self.x_exit, self.y_exit)

        self.x_back = self.screen_width - (1.5 * self.back_txt.get_width())
        self.y_back = self.screen_height - (1.5 * self.back_txt.get_height())
        self.pos_back = (self.x_back, self.y_back)

        
        self.play_rect = self.play_txt.get_rect(topleft = self.pos_play)
        self.inst_rect = self.inst_txt.get_rect(topleft = self.pos_inst)
        self.credits_rect = self.credits_txt.get_rect(topleft = self.pos_credits)
        self.exit_rect = self.exit_txt.get_rect(topleft = self.pos_exit)
        self.back_rect = self.back_txt.get_rect(topleft = self.pos_back)
        

    def main_menu(self):
        
        menu_running = True
        while menu_running:
            self.screen.blit(pygame.transform.smoothscale(self.main_menu_img, self.screen.get_size()), (0,0))
            self.screen.blit(self.play_txt, self.pos_play)
            self.screen.blit(self.inst_txt, self.pos_inst)
            self.screen.blit(self.credits_txt, self.pos_credits)
            self.screen.blit(self.exit_txt, self.pos_exit)

            #checking events for main menu
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = pygame.mouse.get_pos()

                    if self.play_rect.collidepoint(click_pos):
                        pygame.mouse.set_visible(False)
                        astros = Astros()
                        astros.run_game()
                        del astros
                        pygame.mouse.set_visible(True)
                        mixer.music.load('Music/menu.mp3')
                        mixer.music.play(-1)

                    if self.inst_rect.collidepoint(click_pos):
                        self.instructions()
                    
                    if self.credits_rect.collidepoint(click_pos):
                        self.credits()

                    if self.exit_rect.collidepoint(click_pos):
                        self.exit()
                    
            pygame.display.flip()


    def instructions(self):
        
        '''displays the instructions on screen till back is clicked'''
        
        self.inst_img = pygame.image.load('Images/Instructions.png')

        inst_running = True
        while inst_running:
            self.screen.blit(pygame.transform.smoothscale(self.inst_img, self.screen.get_size()), (0,0))
            self.screen.blit(self.back_txt, self.pos_back)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    click_pos = pygame.mouse.get_pos()

                    if self.back_rect.collidepoint(click_pos):
                        inst_running = False

            pygame.display.flip()


    def credits(self):

        '''displays credits on screen till back is clicked'''
        self.credits_img = pygame.image.load('Images/Credits.png')

        credits_running = True
        while credits_running:
            self.screen.blit(pygame.transform.smoothscale(self.credits_img, self.screen.get_size()), (0,0))
            self.screen.blit(self.back_txt, self.pos_back)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    click_pos = pygame.mouse.get_pos()

                    if self.back_rect.collidepoint(click_pos):
                        credits_running = False

            pygame.display.flip()


    def exit(self):
        
        '''exiting the game'''

        exit_txt = self.menu_font.render('Do you really want to quit?', True, (255,255,255))
        x_exit = (self.screen_width/2) - (exit_txt.get_width()/2)
        y_exit = self.screen_height/3
        pos_exit = (x_exit, y_exit)

        #yes text
        yes_txt = self.menu_font.render('Yes', True, (255,255,255))
        x_yes = x_exit
        y_yes = y_exit + 1.5 * exit_txt.get_height()
        pos_yes = (x_yes, y_yes)

        #no text
        no_txt = self.menu_font.render('No', True, (255,255,255))
        x_no = x_exit + 0.9 * exit_txt.get_width()
        y_no = y_exit + 1.5 * exit_txt.get_height()
        pos_no = (x_no, y_no)

        #creating rectangles around it
        yes_rect = yes_txt.get_rect(topleft = pos_yes)
        no_rect = exit_txt.get_rect(topleft = pos_no)

        exit_running = True
        while exit_running:
            self.screen.blit(pygame.transform.smoothscale(self.main_menu_img, self.screen.get_size()), (0,0))
            self.screen.blit(exit_txt, pos_exit)
            self.screen.blit(yes_txt, pos_yes)
            self.screen.blit(no_txt, pos_no)
       
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    click_pos = pygame.mouse.get_pos() 

                    if yes_rect.collidepoint(click_pos):
                        pygame.quit()
                        sys.exit()
                    
                    if no_rect.collidepoint(click_pos):
                        exit_running = False

            pygame.display.flip()


if __name__ == '__main__':

    pygame.init()

    splash = Splash_Screen()            #this will display splash screen in the starting of the game for some seconds
    del splash

    menu = Main_Menu()                  #calling main menu after splash screen
