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

class Game:
    def __init__(self):
        #initiates the game by initiating pygame, setting a screen to draw on
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        #finds the path to the files,links them opens the map text files and and puts data in list
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, "img")
        self.map = Map(path.join(game_folder, "map.txt"))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()

    def new(self):
        #start new game, creates a sprite group variable and draws a map from a txt file
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if (tile == "1"):
                    Wall(self, col, row)
                if (tile == "P"):
                    self.player = Player(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        #game loop
        self.playing = True
        while (self.playing == True):
            self.dt = self.clock.tick(FPS)/ 1000.0
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

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            #draws grey line starting at x cord 0 and ending at the x cord height
             pg.draw.line(self.screen, LIGHTGREY, (x, 0),(x , HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            #draws grey line starting at y cord 0 and ending at the y cord width
             pg.draw.line(self.screen, LIGHTGREY, (0, y),(WIDTH , y))

    def draw(self):
        #game loop - draw
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        #cycles through all instances in self.all+sprites and draws them and applys the camera tracking (so they think they are in the same cordinates
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        #*After* drawing everything(last) makes redrawing smoother by drawing the next screen before displaying it
        pg.display.flip()

    def events(self):
        # handles any and all events (executing an action upon meeting conditions)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()


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
