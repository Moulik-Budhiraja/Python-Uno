from bezier import Curve
import numpy as np
import time
import pygame
from constants import *
from constructors import *
from math import cos, pi
import re
from client import Client
import threading
from logic import GameState, Player
from message import *

pygame.init()

os.system("clear")


class Scale:
    def __init__(self, wi, hi, wf, hf, object, time: float, start_time=0):
        self.wi = wi
        self.hi = hi
        self.wf = wf
        self.hf = hf
        self.object = object
        self.time = time
        self.start_time = start_time

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
        if self.start_time != 0 and self.start_time < time.time() and not self.move:
            self.start()

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
    def __init__(self, xi, yi, xf, yf, object, time: float, start_time=0):
        self.xi = xi
        self.yi = yi
        self.xf = xf
        self.yf = yf
        self.object = object
        self.time = time
        self.start_time = start_time

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
        if self.start_time != 0 and self.start_time < time.time() \
                and not self.move and not self.start_time + self.time < time.time():
            self.start()

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

    def draw(self):
        game.background.draw(self.WIN)
        game.uno_logo.draw(self.WIN)

        game.invalid_ip_alert.draw(self.WIN)
        game.invalid_name_alert.draw(self.WIN)
        game.game_full.draw(self.WIN)

        game.load.draw(self.WIN)

        game.ip_input.draw(self.WIN, (47, 222, 120), (12, 176, 81))
        game.name.draw(self.WIN, (47, 222, 120), (12, 176, 81))

        game.start.draw(self.WIN, (245, 93, 66), (224, 224, 224), 15)
        game.connect.draw(self.WIN, (245, 93, 66), (224, 224, 224), 15)
        game.ready.draw(self.WIN, (52, 235, 86), (0, 168, 31), 15)
        game.unready.draw(self.WIN, (245, 93, 66), (224, 224, 224), 15)
        game.back_to_home.draw(self.WIN, (245, 93, 66), (224, 224, 224), 15)

        try:
            for name in game.player_names:
                name.draw(self.WIN)
        except AttributeError:
            pass

    def update(self):
        pygame.display.update()


class Game:
    def __init__(self):
        self.uno_logo = Image(Assets.UNO_LOGO)
        self.background = Image(Assets.BACKGROUND)
        self.loading = Image(Assets.LOADING)
        self.card_back = Image(Assets.CARD_BACK)

        self.cards = {}

        for c in Assets.CARDS:
            card = Card(c)
            self.cards[card.color + card.number] = card

        print(self.cards)

    def play(self):
        self.alerts = []

        window = Window(Constants.WIDTH, Constants.HEIGHT)

        clock = pygame.time.Clock()

        self.start = Button(pygame.Rect(
            Constants.WIDTH // 2 - 100, Constants.HEIGHT // 2 + 50, 200, 76), "Start", show=True)

        self.uno_logo.x = Constants.WIDTH // 2 - self.uno_logo.width // 2
        self.uno_logo.y = 20

        self.uno_logo_scale = Scale(
            self.uno_logo.width, self.uno_logo.height,
            self.uno_logo.width // 1.5, self.uno_logo.height // 1.5,
            self.uno_logo, 0.4)

        self.uno_logo_transition = Transition(
            self.uno_logo.x, self.uno_logo.y,
            Constants.WIDTH // 2 -
            (self.uno_logo.width // 1.5 // 2), self.uno_logo.y,
            self.uno_logo, 0.4)

        self.invalid_ip_alert = Alert(Constants.WIDTH - 10 - 250,
                                      450, 250, 125, "Invalid IP")

        self.alerts.append(self.invalid_ip_alert)

        self.invalid_ip_transition = Transition(
            10, 600, 10, 475, self.invalid_ip_alert, 0.4)

        self.ip_input = TextBox(400, 60, Constants.WIDTH // 2 - 400 //
                                2, Constants.HEIGHT // 2 - 60 // 2, "Enter IP", 15)

        self.ip_input_transition = Transition(850, self.ip_input.y,
                                              Constants.WIDTH // 2 - self.ip_input.width // 2, self.ip_input.y,
                                              self.ip_input, 0.4)

        self.name = TextBox(400, 60, Constants.WIDTH // 2 - 400 //
                            2, Constants.HEIGHT // 2 + 40, "Enter Name", 15)

        self.name_transition = Transition(850, self.name.y,
                                          Constants.WIDTH // 2 - self.name.width // 2, self.name.y,
                                          self.name, 0.4)

        self.name_transition2 = Transition(self.name_transition.xf, self.name_transition.yf,
                                           -400, self.name_transition.yf,
                                           self.name, 0.4)

        self.invalid_name_alert = Alert(Constants.WIDTH - 10 - 250,
                                        600, 250, 125, "Invalid Name")

        self.alerts.append(self.invalid_name_alert)

        self.invalid_name_transition = Transition(
            10, 600, 10, 475, self.invalid_name_alert, 0.4)

        self.connect = Button(pygame.Rect(-50, 450, 150, 75),
                              "Connect", show=False)

        self.connect_transition = Transition(
            self.connect.x, self.connect.y,
            Constants.WIDTH // 2 - self.connect.width // 2, self.connect.y,
            self.connect, 0.4)

        self.connect_transition2 = Transition(
            self.connect_transition.xf, self.connect_transition.yf,
            850, self.connect_transition.yf,
            self.connect, 0.4)

        self.ip_input_transition2 = Transition(
            self.ip_input_transition.xf, self.ip_input_transition.yf,
            -400, self.ip_input_transition.yf,
            self.ip_input, 0.4)

        self.uno_logo_transition2 = Transition(
            self.uno_logo_transition.xf, self.uno_logo_transition.yf,
            self.uno_logo_transition.xf, -250,
            self.uno_logo, 0.4)

        self.ready = Button(pygame.Rect(
            Constants.WIDTH // 2 - 150 // 2, Constants.HEIGHT - 100, 150, 75), "Ready", show=False)
        self.unready = Button(pygame.Rect(
            Constants.WIDTH // 2 - 150 // 2, Constants.HEIGHT - 100, 150, 75), "Unready", show=False)

        self.ready_transition = Transition(
            self.ready.x, Constants.HEIGHT, self.ready.x, self.ready.y, self.ready, 0.4)
        self.unready_transition = Transition(
            self.unready.x, self.unready.y, self.unready.x, Constants.HEIGHT, self.unready, 0.4)

        self.game_full = Alert(Constants.WIDTH - 10 - 250,
                               450, 250, 125, "Game Full", show=False)
        self.game_full_transition = Transition(
            self.game_full.x, Constants.HEIGHT, self.game_full.x, self.game_full.y, self.game_full, 0.4)

        self.back_to_home = Button(pygame.Rect(
            Constants.WIDTH - 175, Constants.HEIGHT - 100, 150, 75), "Back", show=False)
        self.back_to_home_transition = Transition(
            self.back_to_home.x, Constants.HEIGHT, self.back_to_home.x, self.back_to_home.y, self.back_to_home, 0.4)

        self.load = Loading()

        self.active_textbox = None

        self.wait_for_animations = False
        self.animation_queue = []

        self.game_state = GameState([])

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    try:
                        self.client.disconnect()
                    except AttributeError:
                        pass
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEMOTION:
                    self.start.is_hover(event.pos, enlarge=-10)
                    self.connect.is_hover(event.pos, enlarge=-7)
                    self.ready.is_hover(event.pos, enlarge=-7)
                    self.unready.is_hover(event.pos, enlarge=-7)
                    self.back_to_home.is_hover(event.pos, enlarge=-7)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.start.is_clicked(event.pos):
                            self.load.show_for(0.4)

                            self.start.show = False
                            self.uno_logo_scale.start()
                            self.uno_logo_transition.start()

                            self.ip_input.show = True
                            self.ip_input_transition.start()

                            self.name.show = True
                            self.name_transition.start()

                            self.connect.show = True
                            self.connect_transition.start()

                        if self.ip_input.is_clicked(event.pos):
                            self.active_textbox = self.ip_input

                        if self.name.is_clicked(event.pos):
                            self.active_textbox = self.name

                        if self.back_to_home.is_clicked(event.pos):
                            self.client.disconnect()
                            return

                        if self.ready.is_clicked(event.pos) and not self.ready_frame:
                            msg = Message(self.player.id,
                                          MessageType.PLAYER_READY)
                            self.client.send_msg_queue.append(msg)

                            self.ready.show = False
                            self.unready.show = True

                            self.ready_frame = True

                        if self.unready.is_clicked(event.pos) and not self.ready_frame:
                            msg = Message(self.player.id,
                                          MessageType.PLAYER_UNREADY)
                            self.client.send_msg_queue.append(msg)

                            self.ready.show = True
                            self.unready.show = False

                            self.ready_frame = True

                        if self.back_to_home.is_clicked(event.pos):
                            pass

                        if self.connect.is_clicked(event.pos):
                            if not re.search(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", self.ip_input.text):
                                self.ip_input.text = ""
                                for i in self.alerts:
                                    i.show = False
                                self.invalid_ip_alert.show = True
                                self.invalid_ip_transition.start()

                            elif self.name.text == "":
                                for i in self.alerts:
                                    i.show = False
                                self.invalid_name_alert.show = True
                                self.invalid_name_transition.start()

                            else:
                                for i in self.alerts:
                                    i.show = False

                                self.load.show = True
                                self.client = Client(self.ip_input.text)
                                self.player = []
                                connection = threading.Thread(
                                    target=self.client.connect, args=(self.player,))
                                connection.start()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.active_textbox.deleting = True

                    elif self.active_textbox is not None:
                        self.active_textbox.add_ch(event.unicode)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_BACKSPACE:
                        self.active_textbox.deleting = False

            try:
                if self.client.success:
                    self.client.success = False
                    self.load.show = False
                    self.uno_logo_transition2.start()
                    self.ip_input_transition2.start()
                    self.connect_transition2.start()
                    self.name_transition2.start()
                    self.wait_for_animations = time.time() + 0.4
                    self.just_connected = True
                    self.showing_names = False
                    self.ready.show = True
                    self.ready_transition.start()

                elif threading.active_count() == 1 and self.client.success is False:
                    self.load.show = False
                    for i in self.alerts:
                        i.show = False
                    self.invalid_ip_alert.show = True
                    self.invalid_ip_transition.start()
                    self.client.success = None

            except AttributeError as e:
                # print(e)
                pass

            try:
                if self.client.connected:
                    if type(self.player) == list and len(self.player) > 0:
                        self.player = self.player[0]
                        self.player.name = self.name.text

                        request = Message(
                            self.player.id, MessageType.CONNECT, {"name": self.name.text})
                        self.client.send_msg_queue.append(request)

                    if (not self.wait_for_animations) or self.wait_for_animations < time.time():
                        self.ip_input.show = False
                        self.connect.show = False
                        self.uno_logo.show = False

                        if self.game_state.state == State.UNKNOWN:
                            self.game_state.state = State.LOBBY

                        if not len(self.client.send_msg_queue) == 0:
                            self.load.show_for(0.2)

                    if self.game_state.state != State.UNKNOWN:
                        if not len(self.client.receive_msg_queue) == 0:
                            message = self.client.receive_msg_queue.pop(0)
                            print(message, time.time(), "\n")

                            if message.type == MessageType.PLAYER_LIST:
                                self.game_state.players = [
                                    Player(p["id"], p["name"]) for p in message.content["players"]]
                                try:
                                    self.game_state.ready_players = message.content["ready players"]
                                    print(self.game_state.players)
                                except Exception as e:
                                    raise e

                                if self.game_state.state == State.LOBBY:
                                    # Show players and ready status
                                    if (not self.wait_for_animations or self.wait_for_animations < time.time()):
                                        self.player_names = []
                                        self.name_transitions = []
                                        time_offset = 0

                                        for count, player in enumerate(self.game_state.players):
                                            if player.id in self.game_state.ready_players:
                                                self.player_names.append(
                                                    Text(-400, 25 + 50 * count, player.name.upper(), (52, 235, 86), size=60))
                                            else:
                                                self.player_names.append(
                                                    Text(-400, 25 + 50 * count, player.name.upper(), (235, 64, 52), size=60))

                                        for name in self.player_names:
                                            self.name_transitions.append(
                                                Transition(name.x, name.y, 25, name.y, name, 0.4, time.time() + time_offset))

                                            time_offset += 0.2

                                        for name in self.player_names:
                                            name.show = True

                                        self.wait_for_animations = time.time() + (len(self.name_transitions) * 0.2)
                                        self.just_connected = False

                            elif message.type == MessageType.GAME_START:
                                self.game_state.state = State.PLAYING
                                self.unready_transition.start()

                                # More transitions
                                self.name_transitions = []
                                time_offset = 0

                                for name in self.player_names:
                                    self.name_transitions.append(
                                        Transition(name.x, name.y, -400, name.y, name, 0.4, time.time() + time_offset))

                                    time_offset += 0.2

                                self.wait_for_animations = time.time() + (len(self.name_transitions) * 0.2)

                            elif message.type == MessageType.FORBIDDEN:
                                self.game_full.show = True
                                self.game_full_transition.start()
                                self.ready.show = False

                                self.back_to_home.show = True
                                self.back_to_home_transition.start()

            except AttributeError as e:
                if self.game_state.state == State.LOBBY:
                    raise e
                # print(e)

            self.ready_frame = False

            if self.wait_for_animations > time.time():
                self.load.show_for(0.1)

            self.uno_logo_transition.update()
            self.uno_logo_scale.update()
            self.ip_input.update()
            self.ip_input_transition.update()
            self.connect_transition.update()
            self.invalid_ip_transition.update()
            self.ip_input_transition2.update()
            self.connect_transition2.update()
            self.uno_logo_transition2.update()
            self.load.update()
            self.name.update()
            self.name_transition.update()
            self.invalid_name_transition.update()
            self.name_transition2.update()
            self.ready_transition.update()
            self.unready_transition.update()
            self.game_full_transition.update()
            self.back_to_home_transition.update()

            try:
                for i in self.name_transitions:
                    i.update()
            except AttributeError as e:
                # print(e)
                pass

            window.draw()
            window.update()

            clock.tick(60)


if __name__ == "__main__":
    game = Game()
    while True:
        game.play()
        game = Game()
