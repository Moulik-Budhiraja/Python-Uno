from matplotlib.pyplot import draw
import pygame
from constants import *
from math import cos, pi
import time
import re

pygame.init()


class TextBox:
    def __init__(self, width, height, x=0, y=0, defualt="", max_input=None, show=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.border = pygame.Rect(x, y, width, height)

        self.width = width
        self.height = height

        self.x = x
        self.y = y

        self.text = ""
        self.defualt = defualt
        self.max_input = max_input

        self.show = show
        self.active = False

        self.frame = 0
        self.deleting = False

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.rect.x = value
        self.border.x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.rect.y = value
        self.border.y = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
        self.rect.width = value
        self.border.width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        self.rect.height = value
        self.border.height = value

    def add_ch(self, ch):
        if not self.active:
            return

        if self.max_input is not None and len(self.text) >= self.max_input:
            return

        if re.search(r"^[\w.]+$", ch):
            self.text += ch

    def del_ch(self):
        if not self.active:
            return

        if len(self.text) > 0:
            self.text = self.text[:-1]

    def is_clicked(self, pos):
        if self.rect.collidepoint(pos):
            self.active = True
            return True

        else:
            self.active = False
            return False

    def update(self):
        if self.deleting:
            self.frame += 1

            if self.frame == 1:
                self.del_ch()

            if self.frame >= 15 and self.frame % 3 == 0:
                self.del_ch()

        else:
            self.frame = 0

    def draw(self, screen: pygame.Surface, color, border_color):
        if self.show:
            pygame.draw.rect(screen, color, self.rect)

            if self.active:
                pygame.draw.rect(screen, border_color, self.border, 2)
            else:
                pygame.draw.rect(screen, (180, 180, 180), self.border, 1)

            if self.text != "":
                text = Constants.FONT.render(self.text, True, (36, 36, 36))
                screen.blit(text, (self.x + self.width // 2 - text.get_width() //
                                   2, self.y + self.height // 2 - text.get_height() // 2))
            else:
                text = Constants.FONT.render(
                    self.defualt, True, (79, 79, 79))
                screen.blit(text, (self.x + self.width // 2 - text.get_width() //
                                   2, self.y + self.height // 2 - text.get_height() // 2))


class Loading:
    def __init__(self):
        self.angle = 0

        self.show = False
        self.show_for_time = 0
        self.show_for_start = None

    @property
    def show(self):
        return self._show

    @show.setter
    def show(self, value):
        self._show = value

        if not value:
            self.angle = 0

    def draw(self, screen: pygame.Surface):
        if self.show:
            image = pygame.transform.rotate(Assets.LOADING, self.angle)
            new_rect = image.get_rect(center=Assets.LOADING.get_rect(
                topleft=(Constants.WIDTH - 65, Constants.HEIGHT - 65)).center)

            screen.blit(image, new_rect)

    def update(self):
        if self.show:
            self.angle -= abs(cos(self.angle / 2 * (pi / 180))) * 8 + 1.01

            if self.angle > 720:
                self.angle = 0

        if self.show_for_start is not None:
            if self.show_for_time + self.show_for_start < time.time():
                self.show = False
                self.show_for_start = None

    def show_for(self, seconds):
        self.show_for_time = seconds
        self.show_for_start = time.time()

        self.show = True


class Alert:
    def __init__(self, x, y, height, width, text=None, show=False):
        self.Rect = pygame.Rect(10, 475, 200, 100)

        self.text = text

        self.show = show

    def draw(self, win):
        if not self.show:
            return

        pygame.draw.rect(win, (245, 93, 66), self.Rect, border_radius=15)
        pygame.draw.rect(win, (224, 49, 18), self.Rect, 10, border_radius=15)

        if self.text:
            text = Constants.FONT.render(
                self.text, True, (240, 240, 240))

            win.blit(text, (self.Rect.x + self.Rect.width // 2 - text.get_width() //
                     2, self.Rect.y + self.Rect.height // 2 - text.get_height() // 2))

    @property
    def x(self):
        return self.Rect.x

    @x.setter
    def x(self, value):
        self.Rect = pygame.Rect(value, self.Rect.y,
                                self.Rect.width, self.Rect.height)

    @property
    def y(self):
        return self.Rect.y

    @y.setter
    def y(self, value):
        self.Rect = pygame.Rect(self.Rect.x, value,
                                self.Rect.width, self.Rect.height)


class Button:
    def __init__(self, rect: pygame.Rect, text: str = None, show=True):
        self.rect = rect

        self.text = text

        self.show = show

        self.enlarged = False

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, value):
        self.rect.x = value

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, value):
        self.rect.y = value

    @property
    def width(self):
        return self.rect.width

    @width.setter
    def width(self, value):
        self.rect.width = value

    @property
    def height(self):
        return self.rect.height

    @height.setter
    def height(self, value):
        self.rect.height = value

    def draw(self, win, color, text_color=(240, 240, 240), border_radius=0):
        if not self.show:
            return

        pygame.draw.rect(win, color, self.rect, border_radius=border_radius)

        if self.text:
            text = Constants.FONT.render(
                self.text, True, text_color)

            win.blit(text, (self.rect.x + self.rect.width // 2 - text.get_width() //
                            2, self.rect.y + self.rect.height // 2 - text.get_height() // 2))

    def is_clicked(self, pos):
        if not self.show:
            return False

        return self.rect.collidepoint(pos)

    def is_hover(self, pos, enlarge=0):
        if not self.show:
            return False

        hover = self.rect.collidepoint(pos)

        if enlarge:
            if hover:
                if not self.enlarged:
                    self.rect.inflate_ip(enlarge, enlarge)
                    self.enlarged = True
            else:
                if self.enlarged:
                    self.rect.inflate_ip(-enlarge, -enlarge)
                    self.enlarged = False


class Text:
    def __init__(self, x, y, text, color=(240, 240, 240), font="Lato", size=40, show=False):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.size = size

        self.font = pygame.font.SysFont(font, self.size)

        self.show = show

    def draw(self, win):
        if not self.show:
            return

        text = self.font.render(
            self.text, True, self.color)

        win.blit(text, (self.x, self.y))

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def width(self):
        text = self.font.render(self.text, True, self.color)

        return text.get_width()

    @property
    def height(self):
        text = self.font.render(self.text, True, self.color)

        return text.get_height()


class Card:
    colors = {"0": "R", "1": "Y", "2": "G", "3": "B"}

    def __init__(self, name, x=0, y=0, width=None, height=None):
        self.name = name
        self.path = os.path.join("assets", "cards", name)
        self.image = Image(pygame.image.load(self.path))
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.show = False

        try:
            self.color = self.colors[str(
                int(name[4:6]) - 1)[0] if len(str(int(name[4:6]) - 1)) != 1 else "0"]
        except KeyError:
            if self.name[4:6] in ["41", "42", "43"]:
                self.color = "R"
            elif self.name[4:6] in ["44", "45", "46"]:
                self.color = "Y"
            elif self.name[4:6] in ["47", "48", "49"]:
                self.color = "G"
            elif self.name[4:6] in ["50", "51", "52"]:
                self.color = "B"
            elif self.name[4:6] in ["53", "54", "55", "56"]:
                self.color = None

        if int(self.name[4:6]) in range(1, 41):
            self.number = self.name[5]
        elif int(self.name[4:6]) in range(41, 53):
            if int(self.name[5]) % 3 == 0:
                self.number = "flip"
            elif int(self.name[5]) % 3 == 1:
                self.number = "pick2"
            elif int(self.name[5]) % 3 == 2:
                self.number = "skip"

        elif int(self.name[4:6]) in range(53, 55):
            self.number = "wild"
        elif int(self.name[4:6]) in range(55, 57):
            self.number = "wild4"

    def __repr__(self):
        return f"Card({self.color}{self.number})"

    @property
    def x(self):
        return self.image.x

    @x.setter
    def x(self, value):
        self.image.x = value

    @property
    def y(self):
        return self.image.y

    @y.setter
    def y(self, value):
        self.image.y = value

    @property
    def width(self):
        return self.image.width

    @width.setter
    def width(self, value):
        self.image.width = value

    @property
    def height(self):
        return self.image.height

    @height.setter
    def height(self, value):
        self.image.height = value

    @property
    def show(self):
        return self.image.show

    @show.setter
    def show(self, value):
        self.image.show = value

    def draw(self, win):
        if not self.show:
            return

        self.image.draw(win)
