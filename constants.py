import pygame
from enum import Enum, auto
import os
pygame.init()


class Image:
    def __init__(self, image, x=0, y=0, width=None, height=None):
        self.original_image = image
        self.image = image

        self.x = x
        self.y = y

        self.width = width or self.image.get_width()
        self.height = height or self.image.get_height()

        self.show = True

    @property
    def width(self):
        return self.image.get_width()

    @width.setter
    def width(self, value):
        self.image = pygame.transform.scale(
            self.original_image, (int(value), self.height))

    @property
    def height(self):
        return self.image.get_height()

    @height.setter
    def height(self, value):
        self.image = pygame.transform.scale(
            self.original_image, (self.width, int(value)))

    def draw(self, win):
        if self.show:
            win.blit(self.image, (self.x, self.y))


class Constants:
    WIDTH = 800
    HEIGHT = 600
    FONT = pygame.font.SysFont("Lato", 40)


class Assets:

    BACKGROUND = pygame.transform.scale(pygame.image.load(
        os.path.join("assets", "background.jpg")), (800, 600))

    # Honestly just don't question it
    UNO_LOGO = pygame.transform.scale(
        pygame.image.load(os.path.join("assets", "uno_logo.png")),
        (
            pygame.image.load(os.path.join(
                "assets", "uno_logo.png")).get_width() // 4,
            pygame.image.load(os.path.join(
                "assets", "uno_logo.png")).get_height() // 4
        )
    )

    LOADING = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
        os.path.join("assets", "loading.png")), (50, 50)), 180)

    CARDS = [f"card{i}.png" if i > 9 else
             f"card0{i}.png" for i in range(1, 57)]

    CARD_BACK = pygame.image.load(os.path.join("assets", "back.png"))


class State(Enum):
    LOBBY = auto()
    PLAYING = auto()
    END = auto()
    UNKNOWN = auto()
