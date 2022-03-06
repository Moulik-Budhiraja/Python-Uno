import pygame
from constants import *
from math import cos, pi


class Loading:
    def __init__(self):
        self.angle = 0

        self.show = False

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
