import pygame as pg
import math
from random import uniform, choice, randint
from settings import *
from tilemap import collide_hit_rect
import pytweening as tween
vec = pg.math.Vector2

def collide_with_walls(sprite, group, dir, secondaryGroup = None):
    if dir == 'x':
            hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
            if hits:
                if hits[0].rect.centerx > sprite.hit_rect.centerx:
                    sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 1.99
                if hits[0].rect.centerx < sprite.hit_rect.centerx:
                    sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 1.99
                sprite.vel.x = 0
                sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 1.99
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 1.99
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.img_num = 0
        self.image = game.playerr_img[self.img_num]
        self.img = self.game.playerr_img[self.img_num]
        self.rect = pg.Rect(0, 0, 35, 35)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = (x, y)
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.last_shot = 0
        self.health = PLAYER_HEALTH
        self.last_key = "right"
        self.arrow_dir = vec(0, 1)
        self.arrow_pos = self.pos + vec(30, 0)
        self.ani_speed = 0


    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if (keys[pg.K_LEFT] or keys[pg.K_a]):
            self.vel = vec(-PLAYER_SPEED, 0)
            self.last_key = "left"
            if (self.img_num < len(PLAYERD_IMG)):
                if (self.ani_speed < 8):
                    self.img = self.game.playerl_img[self.img_num]
                    self.ani_speed += 1
                else:
                    self.img = self.game.playerl_img[self.img_num]
                    self.ani_speed = 0
                    self.img_num += 1
            else:
                self.img_num = 0
                self.img = self.game.playerl_img[self.img_num]

        if (keys[pg.K_RIGHT] or keys[pg.K_d]):
            self.vel = vec(PLAYER_SPEED, 0)
            self.last_key = "right"
            if (self.img_num < len(PLAYERR_IMG)):
                if (self.ani_speed < 8):
                    self.img = self.game.playerr_img[self.img_num]
                    self.ani_speed += 1
                else:
                    self.img = self.game.playerr_img[self.img_num]
                    self.ani_speed = 0
                    self.img_num += 1
            else:
                self.img_num = 0
                self.img = self.game.playerr_img[self.img_num]

        if (keys[pg.K_UP] or keys[pg.K_w]):
            self.vel = vec(0, -PLAYER_SPEED)
            self.last_key = "up"
            if (self.img_num < len(PLAYERU_IMG)):
                if (self.ani_speed < 8):
                    self.img = self.game.playeru_img[self.img_num]
                    self.ani_speed += 1
                else:
                    self.img = self.game.playeru_img[self.img_num]
                    self.ani_speed = 0
                    self.img_num += 1
            else:
                self.img_num = 0
                self.img = self.game.playeru_img[self.img_num]

        if (keys[pg.K_DOWN] or keys[pg.K_s]):
            self.vel = vec(0, PLAYER_SPEED)
            self.last_key = "down"
            if (self.img_num < len(PLAYERD_IMG)):
                if (self.ani_speed < 8):
                    self.img = self.game.playerd_img[self.img_num]
                    self.ani_speed += 1
                else:
                    self.img = self.game.playerd_img[self.img_num]
                    self.ani_speed = 0
                    self.img_num += 1
            else:
                self.img_num = 0
                self.img = self.game.playerd_img[self.img_num]

        if (self.last_key == "down"):
            self.arrow_dir = vec(0, 1)
            self.arrow_pos = self.pos + vec(0, 30)
            self.rot = 270
        elif ( self.last_key == "up"):
            self.arrow_dir = vec(0, -1)
            self.arrow_pos = self.pos + vec(0, -30)
            self.rot = 90
        elif ( self.last_key == "left"):
            self.arrow_dir = vec(-1, 0)
            self.arrow_pos = self.pos + vec(-30, 0)
            self.rot = 180
        elif ( self.last_key == "right"):
            self.arrow_dir = vec(1, 0)
            self.arrow_pos = self.pos + vec(30, 0)
            self.rot = 0
        if (keys[pg.K_SPACE]):
            for i in range(len(self.game.inv)):
                if(self.game.inv[i] == 'acorn'):
                    now = pg.time.get_ticks()
                    if (now - self.last_shot > ARROW_RATE):
                        self.last_shot = now
                        Arrow(self.game, self.arrow_pos, self.arrow_dir)
                        self.game.arrow_sounds["shoot"].play()
                        #spawn effect where it needs to be

    def update(self):
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = self.img
        self.rect.center = self.pos
        self.hit_rect.centerx = self.pos.x
        if (self.game.draw_debug == False):
            collide_with_walls(self, self.game.walls, 'x', self.game)
        self.hit_rect.centery = self.pos.y
        if (self.game.draw_debug == False):
            collide_with_walls(self, self.game.walls, 'y', self.game)
        self.rect.center = self.hit_rect.center
        self.pos += self.vel * self.game.dt

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH
        self.speed = choice(MOB_SPEEDS)
        self.target = game.player

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        target_dist = self.target.pos - self.pos
        if target_dist.length_squared() < DETECT_RADIUS**2:
            self.rot = target_dist.angle_to(vec(1, 0))
            self.image = pg.transform.rotate(self.game.mob_img, self.rot)
            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.kill()

class Squirrel(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.squirrels
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.squ_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = self.rect
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH
        self.speed = choice(MOB_SPEEDS)
        self.target = game.player

    def update(self):
        if pg.sprite.spritecollideany(self, self.game.arrows):
            self.health = 0
        if self.health <= 0:
            self.kill()
            self.game.inv.remove('acorn')
            

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image =  game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, name):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.name = name

class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self._layer = ITEMS_LAYER
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.type = type
        self.pos = pos
        self.rect.center = pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

        def update(self):
            # Creates the bobbing motion as well
            offset = BOB_RANGE *(self.tween(self.step / BOB_RANGE) - 0.5)
            self.rect.centery = self.pos.y + offset * self.dir
            self.step += BOB_SPEED
            if (self.step > BOB_RANGE):
                self.step = 0
                self.dir *= -1

class Door(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, name):
        self.groups = game.all_sprites, game.doors
        pg.sprite.Sprite.__init__(self, self.groups)
        self._layer = WALL_LAYER
        self.game = game
        self.image = game.door_img
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.name = name

    def update(self):
        for i in range(len(self.game.inv)):
            if(self.game.inv[i] == 'backpack' and self.game.lvl2loaded == False):
                hits = pg.sprite.spritecollide(self.game.player, self.game.doors, False, collide_hit_rect)
                if hits:
                    self.game.lvl2Time = True

        for i in range(len(self.game.inv)):
            if(self.game.inv[i] == "laptop" and self.game.lvl3loaded == False):
                hits = pg.sprite.spritecollide(self.game.player, self.game.doors, False, collide_hit_rect)
                if hits:
                    self.game.lvl3Time = True

        for i in range(len(self.game.inv)):
            if(self.game.inv[i] == "phone"):
                hits = pg.sprite.spritecollide(self.game.player, self.game.doors, False, collide_hit_rect)
                if hits:
                    self.game.endingTime = True

class Arrow(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self._layer = ARROW_LAYER
        self.groups = game.all_sprites, game.arrows
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.arrow_img
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * ARROW_SPEED
        self.spawn_time = pg.time.get_ticks()
        self.image = pg.transform.rotate(self.game.arrow_img, self.game.player.rot)

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.game.arrow_sounds["hit"].play()
            self.kill()
