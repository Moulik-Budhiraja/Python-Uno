from http.client import FORBIDDEN
import pickle
from enum import Enum, auto


class MessageType(Enum):
    POST_CARD = auto()
    GET_CARDS = auto()
    GET_PLAYERS = auto()
    CONNECT = auto()
    DISCONNECT = auto()
    FORBIDDEN = auto()
    READY = auto()
    RESPONSE = auto()
    BLANK = auto()
    DATA = auto()


class Message:
    def __init__(self, author: str, type: MessageType, content: dict = None, header_length=64, header_format='utf-8') -> None:
        self.author = author
        self.content = content
        self.type = type

        self.HEADER_LENGTH = header_length
        self.HEADER_FORMAT = header_format

    @property
    def length(self) -> int:
        length = len(self.encoded)
        length = str(length).encode(self.HEADER_FORMAT)

        length = length + b" " * (self.HEADER_LENGTH - len(length))

        return length

    @property
    def encoded(self) -> bytes:
        message = pickle.dumps(self)

        return message

    @staticmethod
    def decode(encoded_msg: bytes) -> "Message":
        return pickle.loads(encoded_msg)
