import socket
import threading
from message import Message, MessageType
import uuid
from logic import Player


class Client:
    def __init__(self, server_ip: str, server_port=6969) -> None:
        self.SERVER_IP = server_ip
        self.SERVER_PORT = server_port
        self.ADDR = (self.SERVER_IP, self.SERVER_PORT)

        self.HEADER = 64
        self.FORMAT = "utf-8"

    def connect(self) -> None:
        """
            Establishes a connection to the server"""
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)

        msg = self.receive_msg()

        return Player(msg.content["id"])

    def disconnect(self) -> None:
        """
            Sends a message to the server to disconnect"""
        msg = Message(self.player.id, MessageType.DISCONNECT)
        self.send_msg(msg)

    def receive_msg(self):
        msg_length = self.client.recv(self.HEADER).decode(self.FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = self.client.recv(msg_length)
            msg = Message.decode(msg)

        else:
            msg = Message("Server", MessageType.BLANK)

        return msg

    def send_msg(self, msg: Message):
        """
            Sends a message to the server"""

        self.client.send(msg.length)
        self.client.send(msg.encoded)


if __name__ == "__main__":
    print("Welcome to UNO!")
    client = Client("192.168.50.174")
    client.connect()

    print(client.player.id)

    client.disconnect()
