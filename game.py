from bezier import Curve
import numpy as np
import time
import pygame
from constants import *
from constructors import *
from math import cos, pi

pygame.init()


class Scale:
    def __init__(self, wi, hi, wf, hf, object, time: float):
        self.wi = wi
        self.hi = hi
        self.wf = wf
        self.hf = hf
        self.object = object
        self.time = time

        self.move = False

    def start(self):
        self.move = True

        self.object.width = self.wi
        self.object.height = self.hi

        w_nodes = np.asfortranarray([
            [0, self.time * 0.625, self.time],
            [self.wi, self.wf, self.wf]
        ])

        h_nodes = np.asfortranarray([
            [0, self.time * 0.625, self.time],
            [self.hi, self.hf, self.hf]
        ])

        self.w_curve = Curve(w_nodes, degree=2)
        self.h_curve = Curve(h_nodes, degree=2)

        self.offset = time.time()
        self.end = self.offset + self.time

    def update(self):
        if self.move:
            if time.time() > self.end:
                self.object.width = self.wf
                self.object.height = self.hf

                self.move = False
                return

            current_time = time.time() - self.offset

            w_change = int(self._get_y(
                current_time, self.w_curve)) - self.object.width
            h_change = int(self._get_y(current_time, self.h_curve)
                           ) - self.object.height

            self.object.x -= w_change // 2
            self.object.y -= h_change // 2

            self.object.width = int(self._get_y(current_time, self.w_curve))
            self.object.height = int(self._get_y(current_time, self.h_curve))

    def _get_y(self, x, curve):
        return curve.evaluate_multi(curve.intersect(
            Curve([[x, x], [-500, 1500]], degree=1))[0, :])[1]


class Transition:
    def __init__(self, xi, yi, xf, yf, object, time: float):
        self.xi = xi
        self.yi = yi
        self.xf = xf
        self.yf = yf
        self.object = object
        self.time = time

        self.move = False

    def start(self):
        self.move = True

        self.object.x = self.xi
        self.object.y = self.yi

        x_nodes = np.asfortranarray([
            [0, self.time * 0.625, self.time],
            [self.xi, self.xf, self.xf]
        ])

        y_nodes = np.asfortranarray([
            [0, self.time * 0.625, self.time],
            [self.yi, self.yf, self.yf]
        ])

        self.x_curve = Curve(x_nodes, degree=2)
        self.y_curve = Curve(y_nodes, degree=2)

        self.offset = time.time()
        self.end = self.offset + self.time

    def update(self):
        if self.move:
            if time.time() > self.end:
                self.object.x = self.xf
                self.object.y = self.yf

                self.move = False
                return

            current_time = time.time() - self.offset

            self.object.x = int(self._get_y(current_time, self.x_curve))
            self.object.y = int(self._get_y(current_time, self.y_curve))

    def _get_y(self, x, curve):
        return curve.evaluate_multi(curve.intersect(
            Curve([[x, x], [-500, 1500]], degree=1))[0, :])[1]


class Window:
    def __init__(self, width, height):
        self.WIN = pygame.display.set_mode((width, height))
        pygame.display.set_caption("UNO")

        self.width = width
        self.height = height

        self.start = Button(pygame.Rect(
            self.width // 2 - 100, self.height // 2 + 50, 200, 76), "Start", show=True)

    def draw(self):
        Assets.BACKGROUND.draw(self.WIN)
        Assets.UNO_LOGO.draw(self.WIN)

        game.invalid_ip_alert.draw(self.WIN)
        game.load.draw(self.WIN)

        self.start.draw(self.WIN, (245, 93, 66), (224, 224, 224), 15)

    def update(self):
        pygame.display.update()


class Game:
    def __init__(self):
        self.uno_logo = Image(Assets.UNO_LOGO)
        self.background = Image(Assets.BACKGROUND)
        self.loading = Image(Assets.LOADING)

    def play(self):
        window = Window(Constants.WIDTH, Constants.HEIGHT)

        clock = pygame.time.Clock()

        Assets.UNO_LOGO.x = Constants.WIDTH // 2 - Assets.UNO_LOGO.width // 2
        Assets.UNO_LOGO.y = 20

        self.uno_logo_scale = Scale(
            Assets.UNO_LOGO.width, Assets.UNO_LOGO.height,
            Assets.UNO_LOGO.width // 1.5, Assets.UNO_LOGO.height // 1.5,
            Assets.UNO_LOGO, 1)

        self.invalid_ip_alert = Alert(Constants.WIDTH - 10 - 250,
                                      450, 250, 125, "Invalid IP")
        self.invalid_ip_transition = Transition(
            10, 600, 10, 475, self.invalid_ip_alert, 0.4)

        self.load = Loading()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.MOUSEMOTION:
                    window.start.is_hover(event.pos, enlarge=-10)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if window.start.is_clicked(event.pos):
                            window.start.show = False
                            self.uno_logo_scale.start()

            self.uno_logo_scale.update()
            self.invalid_ip_transition.update()
            self.load.update()

            window.draw()
            window.update()

            clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.play()
