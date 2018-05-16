import pygame as pg
import sys
from settings import *
from random import choice, random
from sprites import *
from os import path
from tilemap import *

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
        self.lvl2Time = False
        self.lvl3Time = False
        self.lvl2loaded = False
        self.lvl3loaded = False
        self.endingTime = False
        self.endOrStart = False

    def draw_text(self, text, font_name, size, color, x, y, align = "nw"):#align is what corner of the rect you want at the given cords
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        # Sets variable for map file, so it can be changed later
        self.mapFile = 'FinalMapTest.tmx'
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'img')
        self.map_folder = path.join(self.game_folder, 'maps')
        self.snd_folder = path.join(self.game_folder, 'snd')
        self.music_folder = path.join(self.game_folder, 'music')
        self.title_font = path.join(self.img_folder, "leadcoat.ttf")
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.inv = []

        #Player Images
        self.playerd_img = [pg.image.load(path.join(self.img_folder, item)).convert_alpha() for item in PLAYERD_IMG]
        self.playeru_img = [pg.image.load(path.join(self.img_folder, item)).convert_alpha() for item in PLAYERU_IMG]
        self.playerl_img = [pg.image.load(path.join(self.img_folder, item)).convert_alpha() for item in PLAYERL_IMG]
        self.playerr_img = [pg.image.load(path.join(self.img_folder, item)).convert_alpha() for item in PLAYERR_IMG]
        self.playerd_img = [pg.transform.scale(item, (TILESIZE, TILESIZE)) for item in self.playerd_img]
        self.playeru_img = [pg.transform.scale(item, (TILESIZE, TILESIZE)) for item in self.playeru_img]
        self.playerl_img = [pg.transform.scale(item, (TILESIZE, TILESIZE)) for item in self.playerl_img]
        self.playerr_img = [pg.transform.scale(item, (TILESIZE, TILESIZE)) for item in self.playerr_img]
        self.player_dmg = []
        for snd in PLAYER_DMG:
            self.player_dmg.append(pg.mixer.Sound(path.join(self.snd_folder, snd)))
        #Mob Images
        self.mob_img = pg.image.load(path.join(self.img_folder, MOB_IMG)).convert_alpha()
        self.mob_img = pg.transform.scale(self.mob_img, (TILESIZE, TILESIZE))
        self.squ_img = pg.image.load(path.join(self.img_folder, SQU_IMG)).convert_alpha()
        self.squ_img = pg.transform.scale(self.squ_img, (TILESIZE * 3, TILESIZE * 2))
        #Projectile Images
        self.arrow_img = pg.image.load(path.join(self.img_folder, ARROWR_IMG)).convert_alpha()
        self.arrow_img = pg.transform.scale(self.arrow_img, (TILESIZE, TILESIZE))

        #Door Images
        self.door_img = pg.image.load(path.join(self.img_folder, DOOR_IMG)).convert_alpha()
        self.door_img = pg.transform.scale(self.door_img, (TILESIZE, TILESIZE))

        #Item Images
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(self.img_folder, ITEM_IMAGES[item])).convert_alpha()
            self.item_images[item] = pg.transform.scale(self.item_images[item], (TILESIZE, TILESIZE))

        #Player Sounds
        #for snd in PLAYER_DMG:
            #self.player_dmg.append(pg.mixer.Sound(path.join(self.snd_folder, snd)))
        self.pickup = pg.mixer.Sound(path.join(self.snd_folder, ITEM_PICKUP))

        self.arrow_sounds = {}
        for type in ARROW_SOUNDS:
            self.arrow_sounds[type] = (pg.mixer.Sound(path.join(self.snd_folder, ARROW_SOUNDS[type])))

    #Starts a new game, creates sprite groups and draws map
    def new(self):
        self.counter =  1
         # Creates the Sprite Groups
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.arrows = pg.sprite.Group()

        # Sets the Map
        self.map = TiledMap(path.join(self.map_folder, self.mapFile))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        # Loads Music
        pg.mixer.music.stop()
        pg.mixer.music.load(path.join(self.music_folder, BG_MUSIC[randint(0,2)]))
        pg.mixer.music.set_volume(0.2)
        pg.mixer.music.play(loops = -1)

        self.player_pct = 1

        # Loads the Map Objects
        for tile_object in self.map.tmxdata.objects:

            obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)

            if (tile_object.name == "player" and self.counter == 1):
                self.player = Player(self, obj_center.x, obj_center.y)
                print "Player Created"
                self.counter += 1

            if tile_object.name == 'mob':
                Mob(self, obj_center.x, obj_center.y)

            if (tile_object.name == "wall"):
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.name)

            if (tile_object.name == "key"):
                Item(self, obj_center, tile_object.name)

            if (tile_object.name == "door"):
                Door(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.name)

            if (tile_object.name == 'acorn'):
                Item(self, obj_center, tile_object.name)

            if (tile_object.name == "backpack"):
                Item(self, obj_center, tile_object.name)

            if (tile_object.name == "exit"):
                Door(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.name)

            if (tile_object.name == "laptop"):
                Item(self, obj_center, tile_object.name)

            if (tile_object.name == "phone"):
                Item(self, obj_center, tile_object.name)
            if (tile_object.name == "squirrel"):
                Squirrel(self, tile_object.x, tile_object.y)

        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False

    def run(self):
        # The Game Loop
        self.playing = True
        pg.mixer.music.play(loops = -1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0 # putting float value fixes issues with Python 2.x
            self.events()
            if(not self.paused):
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # Update the game text, graphics, icons, etc.
        self.all_sprites.update()
        self.camera.update(self.player)

        # Hits variable checks for collisions between different sprites, reacts accordingly
            # Collisions between player and items
        hits = pg.sprite.spritecollide(self.player, self.items, True)
        for hit in hits:
            self.pickup.play()
            hit.kill()
            self.inv.append("{}".format(hit.type))
            # Collisions between Player and Mobs
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            if random() < 0.7:
                choice(self.player_dmg).play()
            self.player_pct -= .1
            self.player.health -= TRAP_DAMAGE
            hit.vel = vec(0, 0)
            if (self.player.health <= 0):
                pg.mixer.music.stop()
                pg.mixer.music.load(path.join(self.music_folder, GO_MUSIC[randint(0,0)]))
                pg.mixer.music.set_volume(0.2)
                pg.mixer.music.play()
                self.playing = False
                self.inv = []
                self.mapFile = 'FinalMapTest.tmx'
                self.endOrStart = True
        if (hits):
            self.player.pos += vec(DMG_KNOCKBACK, 0).rotate(-hits[0].rot)

        if(self.lvl2Time == True):
            self.mapFile = 'FinalMapTest2.tmx'
            self.all_sprites.empty()
            self.walls.empty()
            self.mobs.empty()
            self.doors.empty()
            self.player.kill()
            self.lvl2Time = False
            self.lvl2loaded = True
            self.new()

        if(self.lvl3Time == True):
            self.mapFile = 'FinalMapTest3.tmx'
            self.all_sprites.empty()
            self.walls.empty()
            self.mobs.empty()
            self.doors.empty()
            self.player.kill()
            self.lvl3Time = False
            self.lvl2lvl2loaded = False
            self.new()

        if(self.endingTime == True):
            self.start_es()
            self.all_sprites.empty()
            self.walls.empty()
            self.mobs.empty()
            self.doors.empty()
            self.player.kill()
            self.lvl3loaded = True
            self.endingTime = False
            self.lvl2lvl2loaded = False
            self.playing = False



    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            #draws grey line starting at x cord 0 and ending at the x cord height
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, TILESIZE):
                # draws grey line starting at y cord 0 and ending at the y cord width
                pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    def draw(self):
        # Game Loop Drawing
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.draw_grid()
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            #if(isinstance(sprite, Mob)):
                #sprite.draw_health()
            if(isinstance(sprite, Player)):
                self.screen.blit(sprite.image, self.camera.apply(sprite))
            else:
                self.screen.blit(sprite.image, self.camera.apply(sprite))
            if(self.draw_debug):
                for wall in self.walls:
                    pg.draw.rect(self.screen, RED, self.camera.apply_rect(wall.rect), 1)
            #pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
            # HUD functions
            draw_player_health(self.screen, 10, 10, self.player_pct)
            if(self.paused):
                self.screen.blit(self.dim_screen, (0, 0))
                self.draw_text("Paused", self.title_font, 105, RED, WIDTH / 2, HEIGHT / 2, align="center")
                self.draw_text("You have: " + " ".join(self.inv), self.title_font, 30, GREEN, 100, HEIGHT - 50, align="center")
            pg.display.flip()

    def events(self):
        # Handles any and all events (executing an action upon meeting conditions)
        for event in pg.event.get():
            if(event.type == pg.QUIT):
               self.quit()
            if(event.type == pg.KEYDOWN):
                if (event.key == pg.K_ESCAPE):
                    self.quit()
                if (event.key == pg.K_h):
                    self.draw_debug = not self.draw_debug
                if (event.key == pg.K_p):
                    self.paused = not self.paused

    def show_start_screen(self):
        pg.mixer.music.load(path.join(self.music_folder, INTRO_MUSIC[randint(0,1)]))
        pg.mixer.music.set_volume(0.2)
        pg.mixer.music.play(loops = 1)
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, self.title_font, 48, RED, WIDTH / 2.9, HEIGHT / 4)
        self.draw_text("Press right hand button to shoot, left hand buttons to move", self.title_font, 22, RED, WIDTH / 6, HEIGHT / 2)
        self.draw_text("Press a key to play", self.title_font, 22, RED, WIDTH / 2.6, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.stop()

    def start_cs(self):
        pg.mixer.music.load(path.join(self.music_folder, ALARM))
        pg.mixer.music.set_volume(0.2)
        pg.mixer.music.play(loops = 1)
        self.screen.fill(BGCOLOR)
        self.draw_text("Huh?", self.title_font, 48, RED, WIDTH / 2.3, HEIGHT / 5.5)
        self.draw_text("What time is it?", self.title_font, 22, RED, WIDTH / 2.5, HEIGHT / 3)
        self.draw_text("OH CRAP!!! I'm late for Kiremire's class", self.title_font, 22, RED, WIDTH / 3.7, HEIGHT / 2)
        self.draw_text("*Turns off alarm*", self.title_font, 22, RED, WIDTH / 2.5, HEIGHT / 1.5)
        pg.display.flip()
        self.wait_for_key()

    def start_es(self):
        self.screen.fill(BGCOLOR)
        self.draw_text("Um...", self.title_font, 48, RED, WIDTH / 2.3, HEIGHT / 5.5)
        self.draw_text("Where is everyone?", self.title_font, 22, RED, WIDTH / 2.5, HEIGHT / 3)
        self.draw_text("* looks at phone *", self.title_font, 22, RED, WIDTH / 2.5, HEIGHT / 2)
        self.draw_text("It's Thursday... I'm a freakin' idiot", self.title_font, 22, RED, WIDTH / 3, HEIGHT / 1.5)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.title_font, 100, RED,
                       WIDTH / 2, HEIGHT / 4, align="center")
        self.draw_text("Press any key to return to start menu", self.title_font, 40, WHITE,
                       WIDTH / 2, HEIGHT * 3 / 5, align="center")
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

##################################################################################################
#
#                                           Create and play game
#
##################################################################################################

g = Game()

while (True):
    g.show_start_screen()
    g.start_cs()
    g.new()
    g.run()
    if (g.endOrStart):
        g.show_go_screen()
        g.endOrStart = False
