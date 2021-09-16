#!python main.py
# impelmentation of space invaders
# art Master484  http://m484games.ucoz.com/ 

import pygame
from pygame.locals import *
import random
import os, sys
from button import Button

# Initiate pygame
pygame.init()
pygame.font.init()
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512, devicename=None)
pygame.mixer.init()

# fonts
BG_FONT = pygame.font.Font('assets/fonts/PressStart2P.ttf', 40)
SM_FONT = pygame.font.Font('assets/fonts/PressStart2P.ttf', 30)
XS_FONT = pygame.font.Font('assets/fonts/PressStart2P.ttf', 10)

# set window attributes
WIDTH, HEIGHT = 520, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Wars')

#sound fx
enemy_hit = pygame.mixer.Sound(os.path.join('assets/sounds', 'hit.wav'))
enemy_fires = pygame.mixer.Sound(os.path.join('assets/sounds','laser.wav'))
enemy_fires.set_volume(0.5)
player_hit = pygame.mixer.Sound(os.path.join('assets/sounds', 'ship_hit.wav'))
player_fires = pygame.mixer.Sound(os.path.join('assets/sounds','shoot.wav'))

# icon
# icon = pygame.image.load(os.path.join('assets/images', 'black.png')).convert()
# icon = pygame.display.set_icon(icon)

# buttons
btn1_img = os.path.join('assets/images', 'btn.png')
btn2_img = os.path.join('assets/images', 'btn.png')

#player image
player_img = pygame.transform.scale(pygame.image.load(os.path.join('assets/images', 'player.png')), (64, 64))

#enemies images
enemy1 = pygame.image.load(os.path.join('assets/images', 'enemy1.png'))
enemy2 = pygame.image.load(os.path.join('assets/images', 'enemy2.png'))
enemy3 = pygame.image.load(os.path.join('assets/images', 'enemy3.png'))
enemy4 = pygame.image.load(os.path.join('assets/images', 'enemy4.png'))
enemy5 = pygame.image.load(os.path.join('assets/images', 'enemy5.png'))
enemy6 = pygame.transform.scale(pygame.image.load(os.path.join('assets/images', 'enemy6.png')), (32, 32))
enemy7 = pygame.transform.scale(pygame.image.load(os.path.join('assets/images', 'enemy7.png')), (32, 32))
enemies = [enemy1, enemy2, enemy3, enemy4, enemy5, enemy6, enemy7]

# lasers images
red =  pygame.transform.scale(pygame.image.load(os.path.join('assets/images', 'laser2.png')), (5, 15))
blue = pygame.transform.scale(pygame.image.load(os.path.join('assets/images', 'laser1.png')), (5, 15))

# backgraound image
BG = pygame.transform.scale(pygame.image.load(os.path.join('assets/images','dark_space.jpg')), (WIDTH, HEIGHT))

#colors
BLACK = '#000000'
WHITE = '#FFFFFF'
GREEN = '#00FF00'
RED = '#FF0000'

# enemy count - chsos++
enemy_count = 32
#classic game
rows = 4
cols = 8

# start and end game game variables
mode = ''
countdown = 3
game_over = 0

# player class
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.start_health = health
        self.current_health = health
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        # player velocity
        vel = 8
        # time in milliseconds between player shots
        hold = 500

        game_over = 0
 
        # move player with arrow keys 
        # list of keys pressed 
        keys = pygame.key.get_pressed()
        # left arrow
        if keys[pygame.K_LEFT] and self.rect.left - vel > 0: 
            self.rect.x -= vel
        # RIGHT arrow
        if keys[pygame.K_RIGHT] and self.rect.right + vel  < WIDTH: 
            self.rect.x += vel
        # up arrow
        if keys[pygame.K_UP] and self.rect.top - vel > 0: 
            self.rect.y -= vel
        # down arrow
        if keys[pygame.K_DOWN] and self.rect.bottom + vel < HEIGHT: 
            self.rect.y += vel

        # current time
        now = pygame.time.get_ticks()

        # space-bar to generate lasers and shoot
        if keys[pygame.K_SPACE] and now - self.last_shot > hold: 
            laser = Laser(self.rect.centerx , self.rect.top)
            laser_group.add(laser)
            player_fires.play()
            self.last_shot = now

        # ship mask
        self.mask = pygame.mask.from_surface(self.image)

        #health-bar
        pygame.draw.rect(WIN, RED, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 10))
        if self.current_health > 0:
            pygame.draw.rect(WIN, GREEN, (
                self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.current_health / self.start_health)), 10))
        elif self.current_health <= 0:
            player_hit.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            self.kill()
            game_over = -1
        return game_over

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = red
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.direction = 1
        self.step = 5
    
    def update(self):
        # move a step down 
        self.rect.y -= self.step

        # remove laser from group once off-screen
        if self.rect.bottom < 0:
            self.kill()

        # remove enemies when hit
        if pygame.sprite.spritecollide(self, enemy_group, True):
            player.current_health += 1
            self.kill()
            enemy_hit.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = random.choice(enemies)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.step = 1
        self.step_counter = 0

    # move enemies down
    def update(self):

        if mode == 'chaos':
            self.rect.y += self.step

        # if classic move left and right and down
        if mode == 'classic':
            self.rect.x += self.step 
            self.step_counter += 1
            if abs(self.step_counter) > 75:
                self.rect.y += self.step
                self.step *= -1
                self.step_counter *= self.step


class EnemyLaser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = blue
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.direction = -1
        self.step = 3
    
    def update(self):
        # move 5 px down
        self.rect.y += self.step

        # remove laser from group once off-screen
        if self.rect.top > HEIGHT:
            self.kill()
        # remove enemy laser when hits player
        if pygame.sprite.spritecollide(self, player_group, False, pygame.sprite.collide_mask):
            self.kill()
            # deduct points from player health
            player.current_health -= 10
            enemy_fires.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(explosion)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.images = []
        for i in range(1, 6):
            img = pygame.image.load(os.path.join('assets/images', f'expl{i}.png'))
            if size == 1:
                img = pygame.transform.scale(img, (24, 24))
            if size == 2:
                img = pygame.transform.scale(img, (32, 32))
            if size == 3:
                img = pygame.transform.scale(img, (128, 128))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        # set animation limit
        explosion_limit = 4

        # update explosion animation
        self.counter += 1
        if self.counter >= explosion_limit and self.index < len(self.images) -1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
            self.kill()
        
        # end animation when done
        if self.index > len(self.images) -1 and self.counter >= explosion_limit:
            self.kill()

#sprite groups
player_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
enemy_laser_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

# player 
player = Ship(WIDTH // 2, HEIGHT // 3 * 2, 100)
player_group.add(player)

# create enemies at random positions in a loop
def create_enemies():
    for _ in range(enemy_count):
        x = random.randint(20, WIDTH -20)
        y = random.randint(-2000, -10)
        enemy = Enemy(x, y)
        enemy_group.add(enemy)
    print('Chaos++')


# create rows of enemies at top
def classic_create_enemies():
    for row in range(rows):
        for i in range(cols):
            enemy = Enemy(100 + i * 48 , 50 + row * 48)
            enemy_group.add(enemy)
    print('classic')

# draw text elements
def draw_text(font, text, color, x, y):
    label = font.render(text, True, color)
    WIN.blit(label, (x, y))

run = True
# main loop
def main():
    # redraw interval
    FPS = 60
    global run
    # main loop variables
    clock = pygame.time.Clock()

    # enemy variables
    last_count = pygame.time.get_ticks()

    # game_over: game ended = 0, player won = 1, player lost = -1
    global game_over 

    # game variables
    last_enemy_shot = pygame.time.get_ticks()
    enemy_hold = 1000
    global countdown

    while run:
        clock.tick(FPS)
        
        # draw background
        WIN.blit(BG, (0, 0))

        # hold start until countdown done
        if countdown == 0: 
            # get time now
            now = pygame.time.get_ticks()
            # generate enemy lasers
            if now - last_enemy_shot > enemy_hold and len(enemy_group) > 0:
                firing_enemy = random.choice(enemy_group.sprites())
                if firing_enemy.rect.top >= 0:
                    enemy_laser = EnemyLaser(firing_enemy.rect.centerx, firing_enemy.rect.bottom)
                    enemy_laser_group.add(enemy_laser)
                    last_enemy_shot = now

            # if player destroys all enemies, player wins
            if len(enemy_group) == 0:
                game_over = 1

            # update player. game_over is 0 until player health is 0 or player wins
            if game_over == 0:
                game_over = player.update()

                # call update methods
                laser_group.update()
                enemy_group.update()
                enemy_laser_group.update()

            # win and loss
            else:
                if game_over == -1:
                    draw_text(BG_FONT, 'GAME OVER!', WHITE, int(WIDTH / 2 - 400 / 2), int(HEIGHT / 2 - 20))
                if game_over == 1:
                    draw_text(BG_FONT, 'YOU WON!', WHITE, int(WIDTH / 2 - 150), int(HEIGHT / 2 - 20))
                btn = Button(210, 400, btn1_img, 100, 50)
                btn.draw(WIN)
                draw_text(XS_FONT, 'Again?', BLACK, 85, 420)
                if btn.draw(WIN):
                    game_mneu()

        # countdown to game start
        if countdown > 0 and mode != '':
            # start screen
            draw_text(SM_FONT, 'READY TO PLAY?', WHITE, int(WIDTH / 2 - 210), int(HEIGHT / 2 - 50))
            # countdown
            draw_text(SM_FONT, str(countdown), WHITE, int(WIDTH / 2 - 10), int(HEIGHT / 2))
            # get the time right now
            timer = pygame.time.get_ticks()

            # run countdown
            if timer - last_count > 1000:
                countdown = countdown - 1
                last_count = timer

        # update explosion group
        explosion_group.update()

        # use sprite class draw method to draw group members
        laser_group.draw(WIN)
        enemy_group.draw(WIN)
        player_group.draw(WIN)
        enemy_laser_group.draw(WIN)
        explosion_group.draw(WIN)

        #handle quitting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        pygame.display.update()
    
# game start
def game_mneu():
    global run
    global mode
    global game_over
    game_over = 0
    global countdown

    while mode == '' and countdown > 0:
        # draw background
        WIN.blit(BG, (0, 0))

        # draw title and instructions
        draw_text(BG_FONT, 'SPACE-WARS+', WHITE, 50, 100)
        draw_text(SM_FONT, 'Choose a mode:', WHITE, 50, 300)

        # draw buttons
        # classic button
        btn1 = Button(70, 400, btn1_img, 100, 50)
        btn1.draw(WIN)
        draw_text(XS_FONT, 'Classic', BLACK, 85, 420)

        # exit button
        exit_btn = Button(210, 400, btn1_img, 100, 50)
        exit_btn.draw(WIN)
        draw_text(XS_FONT, 'Exit', BLACK, 240, 420)

        # chaos++ button
        btn2 = Button(350, 400, btn2_img, 100, 50)
        btn2.draw(WIN)
        draw_text(XS_FONT, 'Chaos++', BLACK, 365, 420)

        pygame.display.flip()
        #handle quitting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        # choose mode
        if btn1.draw(WIN):
            enemy_fires.play()
            mode = 'classic'
            classic_create_enemies()
            run = True
            main()

        if btn2.draw(WIN):
            enemy_fires.play()
            mode = 'chaos'
            create_enemies()
            run = True
            main()

        if exit_btn.draw(WIN):
            pygame.quit()
            sys.exit()
game_mneu()
