from http.client import FORBIDDEN
import pickle
from enum import Enum, auto


class MessageType(Enum):
    """What the message is requesting or sending"""
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
    PLAYER_LIST = auto()
    PLAYER_JOINED = auto()
    PLAYER_LEFT = auto()
    PLAYER_READY = auto()
    PLAYER_UNREADY = auto()
    GAME_START = auto()
    PLAYER_ORDER = auto()
    CARDS = auto()
    PLAYER_CARDS = auto()
    ACTIVE_CARD = auto()
    CARD_PLAYED = auto()
    CARD_SELECTED = auto()
    PICKUP_CARDS = auto()
    UNO = auto()
    WINNER = auto()
    PING = auto()


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

    def __repr__(self) -> str:
        return f"<Message {self.type} from {self.author} with content {self.content}>"
