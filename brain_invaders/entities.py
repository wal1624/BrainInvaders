import random
from typing import Any

import main
from media_manager import *
import pygame as pg

TEXT_FONT = "Arial"
TEXT_COLOR = "black"
LETTER_SIZE = 15

PLAYER_MOVE_SPEED = 2

BULLET_FIRE_DELAY = 10
BULLET_VELOCITY = 5

# Initialize groups
ALL = pg.sprite.RenderUpdates()
BULLETS = pg.sprite.Group()
ENEMY_LETTERS = pg.sprite.Group()
COMPONENTS = pg.sprite.Group()

ENEMY_STRINGS = []


class Player(pg.sprite.Sprite):
    GROUPS = ALL

    def __init__(self):
        pg.sprite.Sprite.__init__(self, self.GROUPS)
        raw_img = load_image("starship.png")
        shrink_factor = 4.5
        scaled_img = pg.transform.scale(raw_img,
                                        (raw_img.get_width() / shrink_factor, raw_img.get_height() / shrink_factor))
        self.image = scaled_img
        # self.image.fill("blue")
        self.rect = self.image.get_rect()

    def update(self):
        keystates = pg.key.get_pressed()
        velocity = 0
        if keystates[pg.K_RIGHT] | keystates[pg.K_d]: velocity += PLAYER_MOVE_SPEED
        if keystates[pg.K_LEFT] | keystates[pg.K_a]: velocity -= PLAYER_MOVE_SPEED
        self.rect.x += velocity

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 600:
            self.rect.right = 600





class Bullet(pg.sprite.Sprite):
    GROUPS = ALL, BULLETS

    BULLET_COOLDOWN = 0

    # Called each tick to handle player input/spawning bullets
    @staticmethod
    def bullet_spawn_tick(player: Player):
        if Bullet.BULLET_COOLDOWN > 0:
            Bullet.BULLET_COOLDOWN -= 1
            return

        keystates = pg.key.get_pressed()
        if keystates[pg.K_SPACE]:
            assert Bullet.BULLET_COOLDOWN <= 0
            prect = player.rect
            pos = (prect.centerx - LETTER_SIZE / 4, prect.top)
            spawned_bullet = Bullet(position=pos)
            Bullet.BULLET_COOLDOWN = BULLET_FIRE_DELAY

    def __init__(self, position=(0, 0)):
        # Call the parent class (Sprite) constructor
        pg.sprite.Sprite.__init__(self, self.GROUPS)

        # Set image to filled orange rectangle
        self.image = pg.Surface((LETTER_SIZE / 2, LETTER_SIZE))
        self.image.fill("orange")

        # Set hitbox from image
        self.rect = self.image.get_rect()
        self.rect.move_ip(position)

    def update(self):
        self.rect.y -= BULLET_VELOCITY


class EnemyLetter(pg.sprite.Sprite):
    GROUPS = ALL, ENEMY_LETTERS

    def __init__(self, text, is_evil, evil_visibility=0, position=(0, 0), hit_points=3):
        # Call the parent class (Sprite) constructor
        pg.sprite.Sprite.__init__(self, self.GROUPS)

        self.is_evil = is_evil
        # How many hits it takes to destroy
        self.hp = hit_points
        # Determines how different the color of evil letters are from usual
        # Value from 0-255
        self.evil_visibility = evil_visibility

        color = (255, 255, 255)
        if is_evil:
            non_red = 255 - evil_visibility
            color = (255, non_red, non_red)

        # Generate image based on text
        self.font = pg.font.SysFont(TEXT_FONT, 15)
        self.textSurf = self.font.render(text, True, TEXT_COLOR)
        self.image = pg.Surface((LETTER_SIZE, LETTER_SIZE))
        self.image.fill(color)
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [LETTER_SIZE / 2 - W / 2, LETTER_SIZE / 2 - H / 2])

        self.rect = self.image.get_rect().move(position)

    def hit(self):
        self.hp -= 1
        if (self.hp <= 0):
            self.kill()


class EnemyString():

    def __init__(self, string, evil_visibility=255, position=(0, 0)):
        ENEMY_STRINGS.append(self)

        self.original_string = string
        self.is_destroyed = False

        # List comprehension example for Rohan
        # self.letters = [EnemyLetter(letter) for letter in string]

        # Parse EnemyLetters from provided string
        self.letters = []
        parse_evil = False
        x, y = position
        for letter in string:
            if letter == " ":
                x += LETTER_SIZE
            elif letter == "{":
                parse_evil = True
            elif letter == "}":
                parse_evil = False
            else:
                self.letters.append(EnemyLetter(letter, parse_evil, evil_visibility=evil_visibility, position=(x, y)))
                x += LETTER_SIZE

    def get_rect(self):
        first_rect = self.letters[0].rect
        return pg.rect.Rect(first_rect.x, first_rect.y, len(self.original_string) * LETTER_SIZE, LETTER_SIZE)

    def set_pos(self, position):
        position = list(position)
        for letter in self.letters:
            letter.rect.move_ip(position)

    def is_good(self):
        return not any(let.is_evil and let.alive() for let in self.letters)

    def revive_good_letters(self):
        for letter in self.letters:
            if not letter.alive() and not letter.is_evil:
                letter.add(*letter.GROUPS)

    def drop_letters(self, amount):
        for letter in self.letters:
            letter.rect.y += amount

    def begin_destruction(self, delay=500):
        self.is_destroyed = True
        self.kill_delay = delay

    def kill(self):
        for letter in self.letters:
            letter.kill()
        ENEMY_STRINGS.remove(self)

    def update(self):
        if self.is_destroyed:
            if self.kill_delay <= 0:
                self.kill()
            else:
                self.kill_delay -= 1

    def render_letters(self, screen):
        for letter in self.letters:
            screen.blit(letter.image, letter.rect)