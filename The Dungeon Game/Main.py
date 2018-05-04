##################################################################################################
#
#                                          The Dungeon
#
#
#Jordan Bordelon, Brencen Dela Cruz, Trenton Choate
##################################################################################################
import pygame as pg
import sys
from settings import *
from sprites import *
from os import path
from tilemap import *

# HUD functions
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = BAR_LENGTH * pct
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if (pct > 0.6):
        col = GREEN
    elif (pct > 0.3):
        col = YELLOW
    else:
        col = RED

    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class Game:
    def __init__(self):
        #initiates the game by initiating pygame, setting a screen to draw on
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'maps')
        self.map = TiledMap(path.join(map_folder, 'Map1Test.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.player_img = pg.transform.scale(self.player_img, (TILESIZE, TILESIZE))
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.mob_img = pg.transform.scale(self.mob_img, (TILESIZE, TILESIZE))
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        self.arrow_img = pg.image.load(path.join(img_folder, ARROW_IMG)).convert_alpha()
        self.arrow_img = pg.transform.scale(self.arrow_img, (TILESIZE, TILESIZE))
        # to create visual effects animations
        '''

        self.effect_name = []
        for img in VE:
            self.effect_name.append(pg.image.load(path.join(img_folder, img).convert_alpha))
        '''
    def new(self):
        #start new game, creates a sprite group variable and draws a map from a txt file
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.arrows = pg.sprite.Group()
#        for row, tiles in enumerate(self.map.data):
#            for col, tile in enumerate(tiles):
#                if (tile == "1"):
#                    Wall(self, col, row)
#                if (tile == "P"):
#                    self.player = Player(self, col, row)
#                if (tile == "M"):
#                    Mob(self, col, row)
        for tile_object in self.map.tmxdata.objects:
            if (tile_object.name == "player"):
                self.player = Player(self, tile_object.x, tile_object.y)
            if (tile_object.name == "wall"):
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False

    def run(self):
        #game loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            self.update()
            self.draw()

    def quit(self):
        #exits the game screen after stopping the program
        pg.quit()
        sys.exit()

    def update(self):
        #game loop - update
        self.all_sprites.update()
        self.camera.update(self.player)
        # mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.player.health -= TRAP_DAMAGE
            hit.vel = vec(0, 0)
            if (self.player.health <= 0):
                self.playing = False
        if (hits):
            self.player.pos += vec(DMG_KNOCKBACK, 0).rotate(-hits[0].rot)
        #Arrows hit mob
        hits = pg.sprite.groupcollide(self.mobs, self.arrows, False, True)
        for hit in hits:
            hit.health -= ARROW_DAMAGE
            hit.vel = vec(0, 0)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            #draws grey line starting at x cord 0 and ending at the x cord height
             pg.draw.line(self.screen, LIGHTGREY, (x, 0),(x , HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            #draws grey line starting at y cord 0 and ending at the y cord width
             pg.draw.line(self.screen, LIGHTGREY, (0, y),(WIDTH , y))

    def draw(self):
        #game loop - draw
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.draw_grid()
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            if (isinstance(sprite, Mob)):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if (self.draw_debug):
                pg.draw.rect(self.screen, RED, self.camera.apply_rect(sprite.hit_rect), 1)
        if (self.draw_debug):
            for wall in self.walls:
                pg.draw.rect(self.screen, RED, self.camera.apply_rect(wall.rect), 1)

        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        # HUD functions
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        pg.display.flip()

    def events(self):
        # handles any and all events (executing an action upon meeting conditions)
        for event in pg.event.get():
            if (event.type == pg.QUIT):
                self.quit()
            if (event.type == pg.KEYDOWN):
                if (event.key == pg.K_ESCAPE):
                    self.quit()
                if (event.key == pg.K_h):
                    self.draw_debug = not self.draw_debug


    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


##################################################################################################
#
#                                           Create and play game
#
##################################################################################################

g = Game()
g.show_start_screen()
while (True):
    g.new()
    g.run()
    g.show_go_screen()
