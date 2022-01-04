import sys
import pygame as pg
from entities import *
from media_manager import *
import random, math

COMPONENT_ASSET_DIR = "components"
COMPONENT_SIZE = 100

PROGRESS_PER_FRAME = 1



class Component(pg.sprite.Sprite):
    GROUPS = ALL, COMPONENTS

    def __init__(self, frames_directory, pos=(0, 0)):
        pg.sprite.Sprite.__init__(self, *self.GROUPS)

        self.progress = 0
        self.images = [pg.transform.scale(
            load_image(COMPONENT_ASSET_DIR, frames_directory, file), (COMPONENT_SIZE, COMPONENT_SIZE))
            for file in sorted(get_images_in_dir(COMPONENT_ASSET_DIR, frames_directory))]

        self.image = self.images[0]
        self.rect = self.image.get_rect().move(pos)

    # Class Methods
    def progression(self):
        self.progress += 1
        self.update_image()

    def decrement(self):
        self.progress -= 1
        self.progress = max(self.progress, 0)
        self.update_image()

    def update_image(self):
        img_index = min(math.floor(self.progress / PROGRESS_PER_FRAME), len(self.images) - 1)
        self.image = self.images[img_index]

    def is_complete(self):
        return self.progress >= len(self.images) * PROGRESS_PER_FRAME


def get_incomplete_components():
    return tuple(filter(lambda c: not c.is_complete(), COMPONENTS))
