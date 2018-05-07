#########################################
#
#                   settings
#
#########################################
import pygame as pg
vec = pg.math.Vector2


# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)

# game settings
WIDTH = 800
HEIGHT = 600
FPS = 60
TITLE = "The Dungeon"
BGCOLOR = BLACK

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMG = "tileGreen_39.png"

#play settings
PLAYER_SPEED = 225
PLAYER_ROT_SPEED = 250
PLAYERD_IMG = "downwalk.png"
PLAYERU_IMG = "upwalk.png"
PLAYERL_IMG = "leftwalk.png"
PLAYERR_IMG = "rightwalk.png"
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
PLAYER_HEALTH = 100

#weapon settings
ARROWU_IMG = "Arrowup.png"
ARROWD_IMG = "Arrowdown.png"
ARROWL_IMG = "Arrowleft.png"
ARROWR_IMG = "Arrowright.png"
ARROW_SPEED = 400
ARROW_RATE = 600
ARROW_DAMAGE = 10

#Damage setting
TRAP_DAMAGE = 10
DMG_KNOCKBACK = 20

#mob settings
MOB_IMG = "robot1_hold.png"
MOB_SPEED = 150
MOB_HIT_RECT = pg.Rect(0, 0, 35, 35)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 30
AVOID_RADIUS = 50
DETECT_RADIUS = 400
MOB_SPEEDS = [150, 100, 75, 125]

#visual effects
'''
VE = [all file names in order of display]
effect_duration = 50
'''
# Sounds
INTRO_MUSIC = "Intro.wav"
BG_MUSIC = "Dungeon.wav"
ARROW_SOUNDS = {"shoot": "Arrow_Shoot.wav", "hit": "Arrow_Hit.wav"}
GO_MUSIC = "Game_Over.wav"
PLAYER_DMG = ["Hurt1.wav", "Hurt2.wav", "Hurt3.wav"]
ITEM_PICKUP = "Pickup.wav"
#layers
WALL_LAYER = 1
PLAYER_LAYER = 2
ARROW_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 5
ITEMS_LAYER = 1

# Item settings
ITEM_IMAGES = {"key": "goldenkey.png"}
BOB_RANGE = 15
BOB_SPEED = 0.4

#DOOR_IMG
DOOR_IMG = "door.png"
