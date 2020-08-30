import pygame
import random

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)



width = 600
height = 550
WHITE = (255,255,255)
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

        # Set the player not to walk off screen
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
        self.surf = pygame.image.load('images/1.png').convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (30,30))
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(width + 20, width + 100),
                random.randint(0, height),
            )
        )
    # Move the sprite based on speed
        self.speed = random.randint(6, 6)
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)    
        if self.rect.right < 0:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super(Bullet, self).__init__()
        self.surf = pygame.image.load('images/bullet.png').convert()
        self.surf = pygame.transform.scale(self.surf, (20,20))
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect()

    # 'x' cordinate will shoot the bullet to the right at a speed of 5
    def update(self):
        self.rect.x += 5
        # Bullet will be remove once it hits higher than our width size plus 200
        if self.rect.x >= width + 200:
            self.kill()

def main():
    pygame.mixer.init()
    pygame.init()
    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Andrew's First Game")
    clock = pygame.time.Clock()

    # Keep track of score in the console
    score = 0

    background_image = pygame.image.load('images/sky.png').convert_alpha()
    #Heartbeat by Snowflake (c) copyright 2016 Licensed under a Creative Commons Attribution Noncommercial  (3.0) license. http://dig.ccmixter.org/files/snowflake/53740 Ft: Scomber, George Ellinas, Vidian, Patronski#
    pygame.mixer.music.load("sounds/snowflake_-_Heartbeat.wav")
    # Keep the song playing after it ends
    pygame.mixer.music.play(loops=-1)

    collision_sound = pygame.mixer.Sound('sounds/Explosion+1.wav')


    # Create a custom event for adding new enemy
    ADDENEMY = pygame.USEREVENT + 1
    # Set the timer for new enemy to spawn
    pygame.time.set_timer(ADDENEMY, 200)


    player = Player()
    
    # Group the sprites
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    all_sprites.add(player)

    # Game initialization

    stop_game = False
    while not stop_game:
        for event in pygame.event.get():

            # Event handling
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    collision_sound.play()
                    bullet = Bullet()
                    # Set the bullet cordinates to match with the player.
                    bullet.rect.x = player.rect.x + bullet.rect.width/2
                    bullet.rect.y = player.rect.y  + bullet.rect.height/2
                    bullet_group.add(bullet)
                    all_sprites.add(bullet)
            # Check for QUIT event. If QUIT, then set running to True
            elif event.type == QUIT:
                stop_game = True
            # Add a new enemy
            elif event.type == ADDENEMY:
                # Create the new enemy and addit to to sprite groups
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
            

        for bullet in bullet_group:
            enemy_hit_list = pygame.sprite.spritecollide(bullet, enemies, True)
            for bullet in enemy_hit_list:
                collision_sound.play()
                bullet_group.remove(bullet)
                all_sprites.remove(bullet)
                score += 1

        # Create the score card
        font = pygame.font.Font(None, 36)
        text = font.render("Score: " + str(score), True, WHITE)  
        textpos = text.get_rect(centerx=screen.get_width()/12)     


        # Get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

    

        # Update enemy position
        enemies.update()
        # Update bullet
        bullet_group.update()
        

        # Draw background
        screen.blit(background_image, [0, 0])
        screen.blit(text, textpos)

        # Draw all sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Check if any enemies have collided with the player
        if pygame.sprite.spritecollideany(player, enemies):
            # If so, then remove the player and stop the loop
            collision_sound.play()
            player.kill()
            stop_game = True


        clock.tick(60)
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()
