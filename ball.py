import pygame
from player import Player
import variables

#Ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.ball_images = []
        self.fire_ball = []
        #Loading ball images
        for i in range(12):
            ball_image = pygame.image.load("assets/Ball/Ball" + str(i) +".png")
            ball_image = pygame.transform.scale(ball_image, (variables.BALL_WIDTH,variables.BALL_HEIGHT))
            self.ball_images.append(ball_image)
            if i < 6:
                fire_ball = pygame.image.load("assets/fire_ball/fire_ball" + str(i) +".png")
                fire_ball = pygame.transform.scale(fire_ball, (variables.FIRE_BALL_WIDTH,variables.BALL_HEIGHT))
                self.fire_ball.append(fire_ball)            
        self.surf = pygame.Surface((variables.BALL_WIDTH,variables.BALL_HEIGHT))
        self.current_image = 11
        self.surf = self.ball_images[self.current_image]
        self.rect = self.surf.get_rect()
        self.rect.centerx = variables.SCREEN_WIDTH/2
        self.rect.centery = variables.SCREEN_HEIGHT/2 
        self.direction_speed_x = 0
        self.direction_speed_y = 0
        self.ball_x_last = variables.SCREEN_WIDTH/2
        self.current_image_left = 0
        #Make the ball to move faster when hitting player while running
        self.fast_ball = 0
        self.current_fire = 5
        self.shooting = 0
        self.collide_both = 0

    # Update ball location on screen when moving
    def update(self, all_players):
        self.collide_both = 0
        for player in all_players:   
            collide = pygame.Rect.colliderect(self.rect, player.rect)
            last_x_player , player_x , last_y_player , player_y = player.get_position()
            # TO know in which direction the player is moving
            x_side = (last_x_player - player_x)
            if x_side > 0:
                if (last_y_player - player_y)/x_side == -1 and collide and Ball.in_screen(self):
                    self.direction_speed_y = 2 
                elif (last_y_player - player_y)/x_side == 1 and collide and Ball.in_screen(self):
                    self.direction_speed_y = -2 
            elif x_side < 0:
                if (last_y_player - player_y)/x_side == -1 and collide and Ball.in_screen(self):
                    self.direction_speed_y = -2 
                elif (last_y_player - player_y)/x_side == 1 and collide and Ball.in_screen(self):
                    self.direction_speed_y = 2 
            if collide and Ball.in_screen(self):
                self.collide_both += 1
                if self.rect.right > player.rect.left + 10 and self.rect.right<player.rect.left + 25:
                    self.direction_speed_x = -5 - self.fast_ball -self.shooting
                if self.rect.left < player.rect.right - 10 and self.rect.left>player.rect.right - 25:
                    self.direction_speed_x = 5 + self.fast_ball +self.shooting
            #X = all_players[1].rect.x - self.LastXPlayer
            #Y = all_players[1].rect.y - self.LastYPlayer
        if self.rect.y <= 5:
            self.direction_speed_y = 2
        elif self.rect.y >= variables.SCREEN_HEIGHT - 5:
            self.direction_speed_y = -2
        # if both of the player is touching the ball, move the ball up
        if self.collide_both >1:
            self.direction_speed_y = -2
            self.direction_speed_x = 0
        self.ball_x_last = self.rect.x
        self.rect.move_ip(self.direction_speed_x,self.direction_speed_y)

        if self.rect.left < 0:
            self.direction_speed_x = self.direction_speed_x * -1
        if self.rect.right > variables.SCREEN_WIDTH:
            self.direction_speed_x = self.direction_speed_x * -1
        if self.rect.top <= 0:
            self.direction_speed_y *= -1
        if self.rect.bottom >= variables.SCREEN_HEIGHT:
            self.direction_speed_y *= -1
        Ball.goal_posts(self)

    # Check that the ball stays in the screen
    def in_screen(self):
        if self.rect.right > variables.SCREEN_WIDTH:
            return False
        elif self.rect.left < 0:
            return False
        if self.rect.top < 0:
            return False
        elif self.rect.bottom > variables.SCREEN_HEIGHT:
            return False
        return True
    
    # move the ball when hit above or below the goal posts
    def goal_posts(self):
            if self.rect.right > 950 and self.rect.bottom > 270 and self.rect.bottom < 275:
                self.direction_speed_y = abs(self.direction_speed_y) * -1
            if self.rect.centery >=256 and self.rect.centery < 259 and self.rect.right >=950:
                self.direction_speed_y *= -1
            if self.rect.right > 950 and self.rect.top > 325 and self.rect.top < 330:
                self.direction_speed_y = abs(self.direction_speed_y)
            #Left side
            if self.rect.left < 50 and self.rect.bottom > 270 and self.rect.bottom < 275:
                self.direction_speed_y = abs(self.direction_speed_y) * -1
            if self.rect.centery >=256 and self.rect.centery < 259 and self.rect.left <= 50:
                self.direction_speed_y *= -1
            if self.rect.left < 50 and self.rect.top > 325 and self.rect.top < 330:
                self.direction_speed_y = abs(self.direction_speed_y)

    def default_position(self):
        self.rect.centerx = variables.SCREEN_WIDTH/2
        self.rect.centery = variables.SCREEN_HEIGHT/2

    #  When the player runs a ball go faster
    def ball_hit_runner(self):
        self.fast_ball = 3
    
    # Change ball image every move - images go from right to left and left to right depends on direction of the ball
    def moving_ball(self):
        self.shooting = 0
        if (self.rect.x - self.ball_x_last) > 0:
            self.current_image -= 0.8
            if self.current_image < 0:
                self.current_image = 11
            self.surf = self.ball_images[int(self.current_image)]
        else:
            self.current_image_left += 0.8
            if self.current_image_left > 11:
                self.current_image_left = 0
            self.surf = self.ball_images[int(self.current_image_left)]
        
    # Change ball on fire image every move - images go from right to left and left to right depends on direction of the ball
    # The ball on fire when player shoot the ball using his kick 
    def moving_fire(self):
        self.shooting = 4
        if (self.rect.x - self.ball_x_last) > 0:
            self.current_fire -= 0.2
            if self.current_fire < 0:
                self.current_fire = 5
            self.surf = self.fire_ball[int(self.current_fire)]
        else:
                self.current_fire += 0.2
                if self.current_fire > 5:
                    self.current_fire = 0
                self.surf = self.fire_ball[int(self.current_fire)]