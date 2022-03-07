from constants import State


class Player:
    def __init__(self, id, name=None):
        self.id = id
        self.name = name

        self.cards = []

    def __repr__(self):
        return f"<Player {self.id}, {self.cards}>"


class GameState:
    def __init__(self, players):
        self.players = players

        self.ready_players = []

        self.current_player = None

        self.current_card = None

        self.player_cards = {}

        # lobby, playing, finished
        self.state = State.UNKNOWN
