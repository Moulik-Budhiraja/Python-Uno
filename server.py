import socket
import threading
from message import Message, MessageType
import uuid


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

    def start(self):
        print(f"[STARTING] Server is starting on {self.IP}:{self.PORT}")

        self.server.listen()
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(
                target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

    def handle_client(self, conn, addr):
        player = Player(addr, self.game)

        response = Message("Server", MessageType.DATA, {"id": player.id})
        self.send_to_client(response, conn)

        connected = True
        while connected:
            msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
            if msg_length:
                # Recieve the message
                msg_length = int(msg_length)
                msg = conn.recv(msg_length)
                msg = Message.decode(msg)

                # Handle the message
                if msg.type == MessageType.DISCONNECT:
                    connected = False
                    print(f"[DISCONNECT] {msg.author} disconnected.")

                elif msg.type == MessageType.CONNECT:
                    # Get player info
                    if not self.game.active:
                        self.game.players.append(player)
                        content = [player.dict for player in self.game.players]

                        response = Message(
                            "Server", MessageType.RESPONSE, content)
                        self.send_to_client(response, conn)
                    else:
                        response = Message("Server", MessageType.FORBIDDEN)
                        self.send_to_client(response, conn)

                elif msg.type == MessageType.GET_PLAYERS:
                    pass

                elif msg.type == MessageType.GET_CARDS:
                    pass

                elif msg.type == MessageType.POST_CARD:
                    pass

    def send_to_client(self, msg: Message, conn):
        conn.send(msg.length)
        conn.send(msg.encoded)


class Game:
    def __init__(self, server):
        self.server = server

        self.active = False

        self.players = []

    def start(self):
        pass

    def end(self):
        pass


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
            "players": {
                "name": self.name,
                "id": self.id,
                "cards": self.num_cards
            }
        }


# 558 height
# 1 seperator
# 357 card width
# 2 seperator

if __name__ == "__main__":
    server = Server()
    server.start()
