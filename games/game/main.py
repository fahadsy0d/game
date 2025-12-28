from email.mime import image
import pygame
from sprites import *
from config import *
import sys
import csv

def load_tileset(image, tile_size):
    tiles = []
    image_width, image_height = image.get_size()

    for y in range(0, image_height, tile_size):
        for x in range(0, image_width, tile_size):
            tile = image.subsurface((x, y, tile_size, tile_size))
            tiles.append(tile)

    return tiles

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + SCREEN_WIDTH // 2
        y = -target.rect.centery + SCREEN_HEIGHT // 2

        self.camera = pygame.Rect(x, y, self.width, self.height)


class Game:
    

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.tileset = pygame.image.load("img/gfx/gfx/Overworld.png").convert_alpha()

        
        self.tile_images = load_tileset(self.tileset, TILESIZE)
        self.tile_images[0]  # grass
        self.tile_images[1]  # road
        self.tile_images[2]  # something else



        self.running = True
    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.load_map()  # 👈 FIRST load the map

        self.player = Player(self, 1, 2)

        self.camera = Camera(self.map_width, self.map_height)  # 👈 THEN create camera


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
    
    def load_map(self):
        self.map_width = 0
        self.map_height = 0

        layers = [
            "maps/map_Tile Layer 1.csv",
            "maps/map_Tile Layer 2.csv",
            "maps/map_houses.csv"
        ]

        for layer in layers:
            with open(layer) as f:
                reader = list(csv.reader(f))

                self.map_height = max(self.map_height, len(reader))
                self.map_width = max(self.map_width, len(reader[0]))

                for y, row in enumerate(reader):
                    for x, tile in enumerate(row):
                        if tile != "-1":
                            Block(self, x, y, tile)

        self.map_width *= TILESIZE
        self.map_height *= TILESIZE


    
    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)



    

    def draw(self):
        self.screen.fill(BLACK)

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        self.clock.tick(FPS)
        pygame.display.update()


    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        
        self.running = False
    
    def game_over(self):
        pass

    def intro_screen(self):
        pass


G = Game()
G.intro_screen()
G.new()
while G.running:
    G.main()
    G.game_over()


pygame.quit()
sys.exit()