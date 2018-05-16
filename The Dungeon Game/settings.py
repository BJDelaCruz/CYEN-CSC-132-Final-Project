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

#player settings
PLAYER_SPEED = 175
PLAYER_ROT_SPEED = 250
PLAYERD_IMG = ["downwalk.png", "downwalk1.png", "downwalk2.png", "downwalk3.png"]
PLAYERU_IMG = ["upwalk.png", "upwalk1.png", "upwalk2.png", "upwalk3.png", ]
PLAYERL_IMG = ["leftwalk.png", "leftwalk1.png", "leftwalk2.png", "leftwalk3.png"]
PLAYERR_IMG = ["rightwalk.png", "rightwalk1.png", "rightwalk2.png", "rightwalk3.png", ]
PLAYER_RECT_IMG = "downwalk.png"
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
PLAYER_HEALTH = 100
PLAYER_CONTROLS = [25, 26, 23, 22, 24] # UP DOWN LEFT RIGHT SPACE

#weapon settings
ARROWU_IMG = "Arrowup.png"
ARROWD_IMG = "Arrowdown.png"
ARROWL_IMG = "Arrowleft.png"
ARROWR_IMG = "acorn.png"
ARROW_SPEED = 400
ARROW_RATE = 600
ARROW_DAMAGE = 40

#Platform Settings
PLATFORM_IMG = "platform.png"
PLATFORM_SPEED = 100
#Switch Settings
SWITCH_IMG = "switch_active.png"

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
ALARM = "Alarm.wav"
INTRO_MUSIC = ["Intro2.wav", "Intro.wav", "Intro3.wav"]
BG_MUSIC = ["Dungeon.wav", "Dungeon2.wav", "Dungeon3.wav"]
ARROW_SOUNDS = {"shoot": "Arrow_Shoot.wav", "hit": "Arrow_Hit.wav"}
GO_MUSIC = ["Game_Over.wav", "Game_Over2.wav", "Game_Over3.wav"]
PLAYER_DMG = ["Hurt1.wav", "Hurt2.wav", "Hurt3.wav"]
ITEM_PICKUP = "Pickup.wav"
#layers
WALL_LAYER = 1
PLAYER_LAYER = 1
ARROW_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 5
ITEMS_LAYER = 1

# Item settings
ITEM_IMAGES = {"key": "goldenkey.png", "acorn": "acorn.png", "backpack": "backpack.png", "laptop": "laptop.png"}
BOB_RANGE = 15
BOB_SPEED = 0.4

#DOOR_IMG
DOOR_IMG = "door.png"
