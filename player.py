import pygame
import variables
import json
import time

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self,pos_x,images_player_right,images_player_left,acceptable_move):
        super(Player, self).__init__()
        self.surf = pygame.Surface((variables.PLAYER_WIDTH,variables.PLAYER_HEIGHT))
        self.kid_right = images_player_right
        self.kid_left = images_player_left
        self.current_image = 0
        self.pos_x = pos_x
        self.surf = self.kid_right[self.current_image]
        if self.pos_x > variables.SCREEN_WIDTH/2:
            self.surf = self.kid_left[self.current_image]
        self.acceptable_move = json.loads(acceptable_move)
        self.rect = self.surf.get_rect()
        self.rect = self.rect.inflate(-20, -30) 
        self.rect.x = self.pos_x
        self.rect.y = variables.SCREEN_HEIGHT/2 - variables.BALL_HEIGHT/2
        self.last_x_player = self.rect.x
        self.last_y_player = self.rect.y
        self.run_ability = 0
        self.shoot_ability = 0
        self.frames = 0
        self.adding_speed = 0
        self.shooting = 0
    
    # Get the current position and the last position
    def get_position(self): 
        return self.last_x_player,self.rect.x,self.last_y_player,self.rect.y
    
    # Set last position to be equal to current position
    def set_last_position(self):
        self.last_x_player = self.rect.x
        self.last_y_player = self.rect.y
    
    # Get the ability to shooting and running
    def get_abilities(self):
        return self.run_ability,self.shoot_ability
    
    # Set abilities to  starting point (0)
    def set_abilities(self):
        self.run_ability = 0 
        self.shoot_ability = 0
   
    # Set frame to 0 to check how long the ball will run fast and be on fire
    def shoot(self):
        self.frames = 0
        self.shooting = True
    
    # Set the frames to 0 to check how long the player will run fast 
    def run(self):
        self.frames = 0
        self.adding_speed = 5

    # Update player position when player moving
    def update(self, pressed_keys):
        self.frames += 1
        if self.run_ability<variables.max_run_ability:
            self.run_ability += 0.125
        if self.shoot_ability<variables.max_shoot_ability:
            self.shoot_ability += 0.125

        Player.set_last_position(self)
        if self.frames >= 220:
            self.adding_speed = 0
            self.shooting = False
        if pressed_keys[self.acceptable_move["up"]]:
            self.rect.move_ip(0, -variables.Player_speed -self.adding_speed)

        if pressed_keys[self.acceptable_move["down"]]:
            self.rect.move_ip(0, variables.Player_speed + self.adding_speed)

        if pressed_keys[self.acceptable_move["left"]]:
            self.rect.move_ip(-variables.Player_speed -self.adding_speed, 0)
            self.current_image += 0.25
            if self.current_image >= len (self.kid_left):
                self.current_image = 0
            self.surf = self.kid_left[int(self.current_image)]

        elif pressed_keys[self.acceptable_move["right"]]:
            self.rect.move_ip(variables.Player_speed + self.adding_speed, 0)
            self.current_image += 0.25
            if self.current_image >= len(self.kid_right):
                self.current_image = 0 
            self.surf = self.kid_right[int(self.current_image)]
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > variables.SCREEN_WIDTH:
            self.rect.right = variables.SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0 
        if self.rect.bottom >= variables.SCREEN_HEIGHT:
            self.rect.bottom = variables.SCREEN_HEIGHT  
        if pressed_keys[self.acceptable_move["run"]] and self.run_ability == 150:
            self.run_ability = 0
            Player.run(self)
        if pressed_keys[self.acceptable_move["shoot"]] and self.shoot_ability == 150:
            self.shoot_ability = 0
            Player.shoot(self)
        return self.run_ability, self.shoot_ability

    # For starting the game, set default position
    def set_default_position(self):
        self.rect.x = self.pos_x
        self.rect.y = variables.SCREEN_HEIGHT/2 - variables.BALL_HEIGHT/2
    
    # Check if the player is running
    def is_running(self):
        if self.adding_speed == 5:
            return True
        return False
    
    # Check if the player is shooting
    def is_shoot(self):
        if self.shooting == True:
            return True
        return False