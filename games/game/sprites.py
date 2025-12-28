import pygame
from config import *
import math
import random
import csv


def load_spritesheet(path, frame_w, frame_h):
    sheet = pygame.image.load(path).convert_alpha()
    frames = []

    sheet_width, sheet_height = sheet.get_size()

    rows = sheet_height // frame_h
    cols = sheet_width // frame_w   # extra pixels ignored safely

    for row in range(rows):
        row_frames = []
        for col in range(cols):
            x = col * frame_w
            y = row * frame_h
            frame = sheet.subsurface((x, y, frame_w, frame_h))
            row_frames.append(frame)
        frames.append(row_frames)

    return frames



class Player(pygame.sprite.Sprite):
    def __init__(self, game , x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        
        
        self.animations = load_spritesheet(
            "img/gfx/gfx/character.png",
            PLAYER_SIZE,
            PLAYER_SIZE
        )

        self.direction = "down"
        self.frame = 1
        self.image = self.animations[0][1]


        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'

        self.FRAMES = {
        "walk": slice(0, 4),      # first 4 frames
        "idle": 1,               # middle walk frame
        "attack": slice(0, 6)    # adjust if needed
        }

        self.dir_row = {
            "down": 0,
            "right": 1,
            "up": 2,
            "left": 3
        }

        self.attack_row = {
            "down": 4,
            "up": 5,
            "right": 6,
            "left": 7
        }



        self.rect = self.image.get_rect()
        self.rect.centerx = x * TILESIZE + TILESIZE // 2
        self.rect.bottom = y * TILESIZE + TILESIZE

        self.image = pygame.image.load("img/gfx/gfx/character.png").convert_alpha()
        self.animation_timer = 0
        self.animation_speed = 0.15


    

    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0


    def animate(self):
        row = self.dir_row[self.direction]

        if self.x_change != 0 or self.y_change != 0:
            self.animation_timer += self.animation_speed
            if self.animation_timer >= 1:
                self.animation_timer = 0
                self.frame = (self.frame + 1) % 4
            self.image = self.animations[row][self.frame]
        else:
            self.image = self.animations[row][self.FRAMES["idle"]]

        

    def movement(self):
        keys = pygame.key.get_pressed()

        self.x_change = 0
        self.y_change = 0

        if keys[pygame.K_LEFT]:
            self.x_change = -PLAYER_SPEED
            self.direction = "left"
        elif keys[pygame.K_RIGHT]:
            self.x_change = PLAYER_SPEED
            self.direction = "right"
        elif keys[pygame.K_UP]:
            self.y_change = -PLAYER_SPEED
            self.direction = "up"
        elif keys[pygame.K_DOWN]:
            self.y_change = PLAYER_SPEED
            self.direction = "down"

    def attack(self):
        row = self.attack_row[self.direction]
        # play frames row 4–7

        
    
class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y, tile_id):
        self.game = game
        self._layer = 0
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = self.game.tile_images[int(tile_id)]
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

