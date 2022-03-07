import socket
import threading
from message import Message, MessageType
import uuid
import random


class Server:
    def __init__(self, ip=None, port=6969) -> None:
        self.IP = ip or socket.gethostbyname(socket.gethostname())
        self.PORT = 6969  # Better not already be in use cause its mine now

        self.ADDR = (self.IP, self.PORT)

        self.HEADER = 64
        self.FORMAT = "utf-8"

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)

        self.game = Game(self)

        self.connections = {}

    def start(self):
        print(f"[STARTING] Server is starting on {self.IP}:{self.PORT}")

        self.server.listen()
        while True:
            conn, addr = self.server.accept()

            self.connections[addr] = conn

            thread = threading.Thread(
                target=self.handle_client, args=(conn, addr))
            thread.start()

            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

    def handle_client(self, conn, addr):
        # Send the client their own id
        player = Player(addr, self.game)

        response = Message("Server", MessageType.DATA, {"id": player.id})
        self.send_to_client(response, conn)

        connected = True
        while connected:
            try:
                msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
            except ConnectionResetError:
                connected = False
                self.game.remove_player(player.id)
                self.game.update_players_lists()
                break
            if msg_length:
                # Recieve the message
                msg_length = int(msg_length)
                msg = conn.recv(msg_length)
                msg = Message.decode(msg)

                print(msg)

                # Handle the message
                if msg.type == MessageType.DISCONNECT:
                    connected = False
                    self.game.remove_player(player.id)
                    self.game.update_players_lists()

                elif msg.type == MessageType.CONNECT:
                    # Get player info
                    if not self.game.active:
                        player.name = msg.content["name"]
                        self.game.players.append(player)

                        self.game.update_players_lists()

                    else:
                        response = Message("Server", MessageType.FORBIDDEN)
                        self.send_to_client(response, conn)

                elif msg.type == MessageType.GET_PLAYERS:
                    response = Message("Server", MessageType.PLAYER_LIST,
                                       {
                                           "players": [p.dict for p in self.game.players],
                                           "ready players": [p.id for p in self.game.ready_players]
                                       }
                                       )

                    self.send_to_client(response, conn)

                elif msg.type == MessageType.PLAYER_READY:
                    # ? Not quite sure whats happening here but its very colourful
                    self.game.ready_players.append(player)

                    self.game.update_players_lists()

                    if len(self.game.ready_players) == len(self.game.players) and len(self.game.players) > 1:
                        self.game.start_game()

                elif msg.type == MessageType.PLAYER_UNREADY:
                    # ! this doesn't work
                    self.game.ready_players.remove(player)

                    self.game.update_players_lists()

                elif msg.type == MessageType.GET_CARDS:
                    pass

                elif msg.type == MessageType.POST_CARD:
                    pass

    def send_to_client(self, msg: Message, conn):
        conn.send(msg.length)
        conn.send(msg.encoded)

        print(
            f"[SEND] {msg.author} sent {msg.type} with content {msg.content}")


class Game:
    def __init__(self, server):
        self.server = server

        self.active = False

        self.players = []

        self.ready_players = []

    def start(self):
        pass

    def end(self):
        pass

    def update_players_lists(self):
        for player in self.players:
            response = Message("Server", MessageType.PLAYER_LIST, {
                "players": [p.dict for p in self.players],
                "ready players": [p.id for p in self.ready_players]
            })

            self.server.send_to_client(
                response, server.connections[player.addr])

    def remove_player(self, id):
        for count, i in enumerate(self.players):
            if i.id == id:
                if i in self.ready_players:
                    self.ready_players.remove(i)
                self.players.pop(count)
                break

        if len(self.players) == 0:
            self.active = False

    def start_game(self):
        self.active = True

        random.shuffle(self.players)

        content = {
            "turn order": [p.id for p in self.players]
        }

        response = Message("Server", MessageType.GAME_START, content)

        for player in self.players:
            self.server.send_to_client(
                response, self.server.connections[player.addr])


class Player:
    def __init__(self, addr, game):
        self.addr = addr
        self.game = game

        self.id = uuid.uuid4()
        self.name = None

        self.cards = []

    @property
    def num_cards(self):
        return len(self.cards)

    @property
    def dict(self):
        return {
            "name": self.name,
            "id": self.id,
            "cards": self.num_cards
        }


class Deck:
    def __init__(self):
        self.cards = []
        self.pile = []

        for c in ("R", "Y", "G", "B"):
            for i in range(0, 10):
                if i == 0:
                    self.cards.append(c + "0")
                elif i == 10:
                    self.cards.append(c + "skip")
                elif i == 11:
                    self.cards.append(c + "flip")
                elif i == 12:
                    self.cards.append(c + "draw2")
                else:
                    self.cards.append(c + str(i))
                    self.cards.append(c + str(i))

        for i in range(4):
            self.cards.append("Wwild")
            self.cards.append("Wdraw4")

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

    def reshuffle(self):
        # Take from pile and put in cards
        count = 1
        last_card = None
        for card in self.pile[::-1]:
            if last_card == None:
                last_card = card
                continue

            if card[1:] == last_card[1:]:
                count += 1
                last_card = card
            else:
                break

        self.cards.extend(self.pile[:-count])
        self.pile = self.pile[-count:]

        self.shuffle()

    def deal(self, player):
        pass


if __name__ == "__main__":
    server = Server(ip="127.0.0.1")
    server.start()

