#!/usr/bin/python

# import numpy as np
import pygame
import random

FPS = 60
Width, Height = (600,600)
Player_Color = (50, 100, 200)
Object_Color = (100, 100, 100)
Object_Base_Height = 200
Acc = 0.5

pygame.init()
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

class Objects(pygame.sprite.Sprite):
    def __init__(self, height, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.width, self.height = (100, height)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((Object_Color))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.v = -1.7
        self.x = x
    
    def update(self):
        self.x += self.v
        self.rect.x = self.x

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,40))
        self.image.fill((Player_Color))
        self.rect = self.image.get_rect()
        self.acc = Acc
        self.v = 0
        self.rect.center = (Width/2, Height/2)
        self.last_jump = pygame.time.get_ticks()
        self.jump_delay = 200
    
    def update(self):
        now = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if now - self.last_jump >= self.jump_delay:
                self.v = -7.5 
                self.last_jump = now

        self.rect.centery += self.v
        self.v += self.acc

def kill_obj(obj_sprites):
    for ob in obj_sprites:
        if ob.rect.x < -ob.width:
            ob.kill()

def add_obj(obj_sprites):
    loc = [ob.rect for ob in obj_sprites]
    # yloc = [ob.rect.y for ob in obj_sprites]
    if len(obj_sprites) < 5:
        ob_height = Object_Base_Height + random.uniform(-5, 50)
        X = max(loc)
        if X[1] == 0:
            ob = Objects(ob_height, 
                         X[0] + Width/4 + random.uniform(-5, 15), 
                         Height - ob_height)
        else:
            ob = Objects(ob_height,
                         X[0] + Width/4 + random.uniform(-5, 15), 0)
        all_sprites.add(ob)
        obj_sprites.add(ob)

def display_text(txt, color, size, position, display_screen):    
    font = pygame.font.Font('freesansbold.ttf', size)
    text = font.render(txt, True, color)
    text_rect = text.get_rect()
    text_rect.centerx, text_rect.centery = position
    display_screen.blit(text, text_rect)

def init_game_settings():
    all_sprites = pygame.sprite.Group()
    obj_sprites = pygame.sprite.Group()
    bird = Player()
    all_sprites.add(bird)
    
    # Make initial objects:
    for i in range(5):
        ob_height = Object_Base_Height + random.normalvariate(0, 15)
        ob = Objects(ob_height,
                     Width * 3/4 + i * Width/4 + random.normalvariate(0, 5), 
                     i%2 * (Height - ob_height))
        all_sprites.add(ob)
        obj_sprites.add(ob)
    
    return all_sprites, obj_sprites, bird

def show_wait_screen():
    # display_text('Game Over', (255,255,255), 30, (Width/2, Height/2), screen)
    pygame.init()
    waiting = True
    while waiting:
        display_text('Press Enter key to start!', (20,240,240), 20, (Width/2, Height * 3/4), screen)
        clock.tick(FPS)
        # screen.fill((0, 10, 20))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    waiting = False

COUNT = 0
game_start = True
run = True
while run:
    if game_start:
        all_sprites, obj_sprites, bird = init_game_settings()
        COUNT = 0
        show_wait_screen()
        game_start = False
        
    clock.tick(FPS)
    screen.fill((0, 10, 20))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
               
    all_sprites.update()
    kill_obj(obj_sprites)
    add_obj(obj_sprites)
    
    all_sprites.draw(screen)
    
    # Score Update:
    for ob in obj_sprites:
        if ob.rect.x < bird.rect.x:
            COUNT += 1
    score = COUNT//FPS
    
    # Check Collision:
    bird_hit = pygame.sprite.spritecollide(bird, obj_sprites, False,
                                             collided = pygame.sprite.collide_rect_ratio(1))
    if bird_hit:
        display_text('Game Over', (255,255,255), 30, (Width/2, Height/2), screen)
        display_text('Score: {}'.format(score), (240,25,100), 20, (Width/2, Height/4), screen)
        bird.kill()
        game_start = True

    # GAME OVER:
    if bird.rect.midbottom[1] > Height:
        display_text('Game Over', (255,255,255), 30, (Width/2, Height/2), screen)
        display_text('Score: {}'.format(score), (240,25,100), 20, (Width/2, Height/4), screen)
        bird.kill()
        game_start = True
    
    display_text('Score: {}'.format(score), (255,255,255), 12, (50, 10), screen)
    pygame.display.update()

pygame.quit()
