import pygame
import random



from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

width = 500
height = 500
# blue_color = (97, 159, 182)
# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load('images/tef_claymore.png').convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (40,40))
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)    

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= height:
            self.rect.bottom = height   

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load('images/fly1.png').convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (25,25))
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(width + 20, width + 100),
                random.randint(0, height),
            )
        )
        self.speed = random.randint(5, 20)
    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)    
        if self.rect.right < 0:
            self.kill()
# class Cloud(pygame.sprite.Sprite):
#     def __init__(self):
#         super(Cloud, self).__init__()
#         self.surf = pygame.image.load('images/cloudy.png').convert_alpha()
#         self.surf = pygame.transform.scale(self.surf, (30,30))
#         self.surf.set_colorkey((0,0,0), RLEACCEL)
#         # The starting position is randomly generated
#         self.rect = self.surf.get_rect(
#             center=(
#                 random.randint(width + 20, width+ 100),
#                 random.randint(0, height),
#             )
#         )
#     def update(self):
#         self.rect.move_ip(-5, 0)
#         if self.rect.right < 0:
#             self.kill()
def main():
    pygame.mixer.init()
    pygame.init()
    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('My Game')
    clock = pygame.time.Clock()
    background_image = pygame.image.load('images/sky.png').convert_alpha()
    #eartbeat by Snowflake (c) copyright 2016 Licensed under a Creative Commons Attribution Noncommercial  (3.0) license. http://dig.ccmixter.org/files/snowflake/53740 Ft: Scomber, George Ellinas, Vidian, Patronski#
    pygame.mixer.music.load("sounds/snowflake_-_Heartbeat(online-audio-converter.com).wav")
    pygame.mixer.music.play(loops=-1)
    # Create a custom event for adding new enemy
    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 250)
    # Create custom events for adding a new enemy and a cloud
    ADDCLOUD = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDCLOUD, 1000)

    # Instantiate player. Right now, this is just a rectangle.
    player = Player()
    
    enemies = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Game initialization

    stop_game = False
    while not stop_game:
        for event in pygame.event.get():

            # Event handling
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    stop_game = True
            # Check for QUIT event. If QUIT, then set running to True
            elif event.type == pygame.QUIT:
                stop_game = True
            # Add a new enemy
            elif event.type == ADDENEMY:
                # Create the new enemy and addit to to sprite groups
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy) 
            # Add a new cloud
            # elif event.type == ADDCLOUD:
            #     # Create the new cloud and add it to sprite groups
            #     new_cloud = Cloud()
            #     clouds.add(new_cloud)
            #     all_sprites.add(new_cloud)    

        # Get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

    

        # Update enemy position
        enemies.update()
        clouds.update()
        


        # Game logic

        # Draw background
        screen.blit(background_image, [0, 0])

        # Draw all sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Check if any enemies have collided with the player
        if pygame.sprite.spritecollideany(player, enemies):
            # If so, then remove the player and stop the loop
            player.kill()
            stop_game = True

        # Game display
        
        # Put the center of surf at the center of the display
        # surf_center = (
        #     (width-surf.get_width())/2,
        #     (height-surf.get_height())/2
        # )
        # Draw surf at the new coordinates
        # screen.blit(surf, surf_center)
        clock.tick(30)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
