import time
import pygame
import pygame.locals
import variables
import player
import ball
import json
# Game class
class Game(object):
    def load_images(self, path):
        images = []
        for i in range(8):
            image = pygame.image.load(path + str(i) +".png")
            images.append(pygame.transform.scale(image, (70, 100)))
        return images
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()  
        pygame.display.set_caption('Football Shoot')
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((variables.SCREEN_WIDTH, variables.SCREEN_HEIGHT))
        accept_right = json.dumps({"left" : pygame.locals.K_LEFT,"right" : pygame.locals.K_RIGHT,"up" : pygame.locals.K_UP,"down" : pygame.locals.K_DOWN,"run" : pygame.locals.K_SPACE,"shoot" : pygame.locals.K_RALT})
        accept_left = json.dumps({"left" : pygame.K_a,"right" : pygame.K_d,"up" : pygame.K_w,"down" : pygame.K_s,"run":pygame.locals.K_q,"shoot" : pygame.locals.K_TAB})
        self.player_right = player.Player(860,self.load_images("assets/RunnerOrange/right"),
                                            self.load_images("assets/RunnerOrange/left"),accept_right)
        self.player_left = player.Player(100,self.load_images("assets/RunnerBlue/Right"),
                                            self.load_images("assets/RunnerBlue/Left"),accept_left)
        self.ball = ball.Ball()
        # Variable to keep the main loop running
        self.running = True
        self.bg = pygame.image.load("assets/field.png")
        self.field = pygame.transform.scale(self.bg, (variables.SCREEN_WIDTH, variables.SCREEN_HEIGHT))
        header = pygame.font.SysFont('Comic Sans MS', 40)
        self.header_surface = header.render('Football', False, (0, 0, 0))
        header_width = self.header_surface.get_rect().width
        self.header_center = (variables.SCREEN_WIDTH - header_width) /2 
        self.score_text = pygame.font.SysFont('Comic Sans MS', 20)
        self.goal_text = pygame.font.SysFont('Comic Sans MS', 150)
        self.right_score = variables.Score
        self.left_score = variables.Score
        self.score_right_surface = self.score_text.render("Score: " + str(self.right_score), 1,variables.black)
        self.score_left_surface = self.score_text.render("Score: " + str(self.left_score), 1,variables.black)
        #Screen quarter with text for placing the text right
        left_text_width = self.score_left_surface.get_rect().width
        self.screen_quarter = variables.SCREEN_WIDTH/4 - left_text_width/2
        self.screen_3rd_quarter = (variables.SCREEN_WIDTH/4)*3 - left_text_width/2
        self.all_players = []
        self.goal_animation_list = []
        self.game_over_animation = []            
        for i in range(0,139):
            if i < 52:
                image_gm_over = pygame.image.load("assets/game_over/frame_"+str("%02d"% i)+"_delay-0.2s.gif")
                self.game_over_animation.append(pygame.transform.scale(image_gm_over,(variables.SCREEN_WIDTH, variables.SCREEN_HEIGHT)))
            image = pygame.image.load("assets/goal_animation/frame_"+str("%03d"% i)+"_delay-0.04s.gif")
            self.goal_animation_list.append(pygame.transform.scale(image, (variables.SCREEN_WIDTH, variables.SCREEN_HEIGHT)))
        
        self.all_players.append(self.player_right)       
        self.all_players.append(self.player_left)
   
    # When starting the game/starting new game
    def reset_game(self):
        self.left_score = 0
        self.right_score = 0
        self.score_left_surface = self.score_text.render("Score: " + str(self.left_score), 1,variables.black)
        self.score_right_surface = self.score_text.render("Score: " + str(self.right_score), 1,variables.black)
        self.player_right.set_abilities()
        self.player_left.set_abilities()
        pygame.display.flip()
    
    # When game over
    def game_over(self):
        frame_game_over = 0
        pygame.mixer.music.load("assets/Sounds/game_over.mp3")
        pygame.mixer.music.play(-1)
        again = pygame.image.load("assets/again.png")
        again_image = pygame.transform.scale(again, (60, 60))
        home = pygame.image.load("assets/back_home.png")
        home_image = pygame.transform.scale(home, (80, 80))
        home_image_rect = home_image.get_rect(center=(variables.SCREEN_WIDTH/2-50,550))
        again_image_rect = home_image.get_rect(center=(variables.SCREEN_WIDTH/2+30,560))
        game_over_loop = True
        while game_over_loop:
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                # Check for KEYDOWN event
                if event.type == pygame.locals.KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                    if event.key == pygame.locals.K_ESCAPE:
                        self.running = False
                        game_over_loop = False
                        return
                # Check for QUIT event. If QUIT, then set running to false.
                elif event.type == pygame.locals.QUIT:
                    self.running = False
                    game_over_loop = False
                    return
            if home_image_rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] ==1:
                    game_over_loop = False

                    Game.reset_game(self)
                    if Game.open_page(self) == False:
                        self.running = False
                    pygame.mixer.music.load("assets/Sounds/BackgroundSound.mp3")
                    pygame.mixer.music.play(-1)
            elif again_image_rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1:
                    game_over_loop = False
                    Game.reset_game(self)
                    pygame.mixer.music.load("assets/Sounds/BackgroundSound.mp3")
                    pygame.mixer.music.play(-1)
            if frame_game_over >= 51:
                frame_game_over = 0
            self.screen.blit(self.game_over_animation[int(frame_game_over)],(0,0))
            self.screen.blit(again_image,again_image_rect)
            self.screen.blit(home_image,(home_image_rect))
            frame_game_over += 0.01
            pygame.display.flip()
            self.clock.tick(60)
     
    def goal(self):
        if self.ball.rect.right > 950 and self.ball.rect.centery >260 and self.ball.rect.centery < 338:
            self.ball.default_position()
            self.left_score += 1
            self.ball.direction_speed_x = 0
            self.ball.direction_speed_y = 0
            self.score_left_surface = self.score_text.render("Score: " + str(self.left_score), 1,variables.black)
            Game.goal_animation(self)    
            return True
        elif self.ball.rect.left < 50 and self.ball.rect.centery >260 and self.ball.rect.centery < 338:   
            self.ball.rect.centerx = variables.SCREEN_WIDTH/2
            self.ball.rect.centery= variables.SCREEN_HEIGHT/2 
            self.right_score += 1
            self.ball.direction_speed_x = 0
            self.ball.direction_speed_y = 0
            self.score_right_surface = self.score_text.render("Score: " + str(self.right_score), 1,variables.black)
            Game.goal_animation(self) 
            return True
        return False

    # Animation pops up when a player scores a goal 
    def goal_animation(self):
        self.player_left.set_default_position()
        self.player_right.set_default_position()
        #text = self.goal_text.render("GOAL!!!", True, variables.green)
        #text_rect = text.get_rect(center=(variables.SCREEN_WIDTH/2, variables.SCREEN_HEIGHT/2))
        pygame.mixer.music.load("assets/Sounds/Goal.mp3")
        pygame.mixer.music.play(0)
        self.ball.default_position()
        for i in self.goal_animation_list:
            self.screen.blit(i,(0,0))
            time.sleep(0.05)
            pygame.display.flip()
        pygame.mixer.music.load("assets/Sounds/BackgroundSound.mp3")
        pygame.mixer.music.play(-1)
    # When game starts     
    def run(self):
        pygame.mixer.music.load("assets/Sounds/BackgroundSound.mp3")
        pygame.mixer.music.play(-1)
        while self.running:
            # for loop through the event queue
            for event in pygame.event.get():
                # Check for KEYDOWN event
                if event.type == pygame.locals.KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                    if event.key == pygame.locals.K_ESCAPE:
                        self.running = False
            # Check for QUIT event. If QUIT, then set running to false.
                elif event.type == pygame.locals.QUIT:
                    self.running = False
            pressed_keys = pygame.key.get_pressed()
            # Update the player sprite based on user keypresses
            Game.goal(self)
            if self.left_score ==5 or self.right_score ==5:
                Game.game_over(self)
            if player.Player.is_running(self.player_right) or player.Player.is_running(self.player_left):
                ball.Ball.ball_hit_runner(self.ball)
            if player.Player.is_shoot(self.player_left) or player.Player.is_shoot(self.player_right):
                ball.Ball.moving_fire(self.ball)
            else:
                ball.Ball.moving_ball(self.ball)
            self.screen.blit(self.field, (0, 0))   
            # Update the player sprite based on user keypresses
            self.player_right.update(pressed_keys)
            self.player_left.update(pressed_keys)
            # Update ball sprites based on hitting walls and players
            self.ball.update(self.all_players)
            # Image of shooting beside shoot bar
            shoot = pygame.image.load("assets/Shoot.png")
            shoot_image = pygame.transform.scale(shoot, (40, 40))
            self.screen.blit(shoot_image,(200,15))
            # Image of running beside the running bar
            run = pygame.image.load("assets/run.png")
            run_image = pygame.transform.scale(run, (40, 40))
            self.screen.blit(run_image,(200,50))
            # Get abilities of all players
            run_ability_right , shoot_ability_right = self.player_right.get_abilities()
            run_ability_left , shoot_ability_left = self.player_left.get_abilities()
            # Draw the bars at the top
            pygame.draw.rect(self.screen,variables.green,(40,60,run_ability_left,20))
            pygame.draw.rect(self.screen,variables.white,(40,60,150,20),2)
            bar = pygame.Surface((150,18))
            bar.fill(variables.red)
            self.screen.blit(bar , (40,30))
            pygame.draw.rect(self.screen,variables.green,(40,30,shoot_ability_left,18))
            self.screen.blit(run_image,(750,50))
            self.screen.blit(shoot_image,(750,15))
            pygame.draw.rect(self.screen,variables.green,(810,60,run_ability_right,20))
            pygame.draw.rect(self.screen,variables.white,(810,60,150,20),2)
            bar = pygame.Surface((150,18))
            bar.fill(variables.red)
            self.screen.blit(bar , (810,30))
            pygame.draw.rect(self.screen,variables.green,(810,30,shoot_ability_right,18))
            # Draw players
            self.screen.blit(self.player_right.surf, self.player_right.rect)
            self.screen.blit(self.player_left.surf, self.player_left.rect)
            # Draw ball
            self.screen.blit(self.ball.surf, self.ball.rect)
            # Draw header
            self.screen.blit(self.header_surface, (self.header_center,40))
            # Draw scores
            self.screen.blit(self.score_right_surface,(self.screen_3rd_quarter-100,60))
            self.screen.blit(self.score_left_surface,(self.screen_quarter+100,60)) 
            pygame.display.flip()
            self.clock.tick(60)
    # Home page, before the game starts
    def open_page(self):
        pygame.mixer.music.load("assets/Sounds/front_music.mp3")
        pygame.mixer.music.play(-1)
        home_run = True
        start_bg = []
        curr_img = 6
        up_down_img =-0.02
        for i in range(0,7):
            start_bg.append("assets/open_gif/open_bg" + str(i) + ".gif")
        start_img = pygame.image.load('assets/start.png').convert_alpha()
        start_img = pygame.transform.scale(start_img,(200,50))
        start_img_rect = start_img.get_rect(center=(variables.SCREEN_WIDTH/2,variables.SCREEN_HEIGHT/2))
        guide = pygame.image.load("assets/guide.png").convert_alpha()
        guide = pygame.transform.scale(guide,(100,30))
        guide_rect = guide.get_rect(center=(variables.SCREEN_WIDTH/2,variables.SCREEN_HEIGHT/2+250))   
        guide_text = pygame.image.load("assets/guide_text.png").convert_alpha()
        guide_text = pygame.transform.scale(guide_text,(800,400))
        guide_text_rect = guide_text.get_rect(center=(variables.SCREEN_WIDTH/2,variables.SCREEN_HEIGHT/2))
        while home_run:
            bg = pygame.image.load(start_bg[int(curr_img)])
            moving_bg = pygame.transform.scale(bg, (variables.SCREEN_WIDTH, variables.SCREEN_HEIGHT))
            self.screen.blit(moving_bg,(0,0))
            self.screen.blit(guide,(guide_rect))
            curr_img =curr_img + up_down_img 
            if curr_img <= 0:
                up_down_img = 0.02
            elif curr_img >=6:
                up_down_img = -0.02
            for event in pygame.event.get():
                # Check for KEYDOWN event
                if event.type == pygame.locals.KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                    if event.key == pygame.locals.K_ESCAPE:
                        return False
            # Check for QUIT event. If QUIT, then set running to false.
                elif event.type == pygame.locals.QUIT:
                    return False
            self.screen.blit(start_img,(start_img_rect))
            pos = pygame.mouse.get_pos()
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_SPACE] or pressed_keys[pygame.K_KP_ENTER]:
                return True
            if start_img_rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] ==1:
                    return True
            if guide_rect.collidepoint(pos): 
                self.screen.blit(guide_text,(guide_text_rect))
            pygame.display.flip()
            self.clock.tick(60)
