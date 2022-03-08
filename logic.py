from constants import State, Constants


class Player:
    def __init__(self, id, name=None):
        self.id = id
        self.name = name

        self.hand = []

    def __repr__(self):
        return f"<Player {self.id}, {self.cards}>"


class GameState:
    RIGHT_OFFSET = 40
    TOP_OFFSET = 10
    LEFT_OFFSET = 10

    def __init__(self, players):
        self.players = players

        self.ready_players = []

        self.current_player = None

        self.current_card = None

        self.player_cards = {}

        self.turn_order = []

        self.turn = None
        # lobby, playing, finished
        self.state = State.UNKNOWN

        # Don't worry I didn't have to write this all out
        self.player_positions = {
            2: {1: (Constants.WIDTH // 2, self.TOP_OFFSET)},
            3: {1: (self.LEFT_OFFSET, Constants.HEIGHT // 2), 2: (Constants.WIDTH - self.RIGHT_OFFSET, Constants.HEIGHT // 2)},
            4: {1: (self.LEFT_OFFSET, Constants.HEIGHT // 2), 2:  (Constants.WIDTH // 2, self.TOP_OFFSET), 3: (Constants.WIDTH - self.RIGHT_OFFSET, Constants.HEIGHT // 2)},
            5: {1: (self.LEFT_OFFSET, Constants.HEIGHT // 2), 2: (Constants.WIDTH // 3, self.TOP_OFFSET), 3: (Constants.WIDTH // 3 * 2, self.TOP_OFFSET), 4: (Constants.WIDTH - self.RIGHT_OFFSET, Constants.HEIGHT // 2)},
            6: {1: (self.LEFT_OFFSET, Constants.HEIGHT // 2), 2: (Constants.WIDTH // 4, self.TOP_OFFSET), 3: (Constants.WIDTH // 4 * 2, self.TOP_OFFSET), 4: (Constants.WIDTH // 4 * 3, self.TOP_OFFSET), 5: (Constants.WIDTH - self.RIGHT_OFFSET, Constants.HEIGHT // 2)},
            7: {1: (self.LEFT_OFFSET, Constants.HEIGHT // 3 * 2), 2: (self.LEFT_OFFSET, Constants.HEIGHT // 3), 3: (Constants.WIDTH // 3, self.TOP_OFFSET), 4: (Constants.WIDTH // 3 * 2, self.TOP_OFFSET), 5: (Constants.WIDTH - self.RIGHT_OFFSET, Constants.HEIGHT // 3), 6: (Constants.WIDTH - self.RIGHT_OFFSET, Constants.HEIGHT // 3 * 2)},
            8: {1: (self.LEFT_OFFSET, Constants.HEIGHT // 3 * 2), 2: (self.LEFT_OFFSET, Constants.HEIGHT // 3), 3: (Constants.WIDTH // 4, self.TOP_OFFSET), 4: (Constants.WIDTH // 4 * 2, self.TOP_OFFSET), 5: (Constants.WIDTH // 4 * 3, self.TOP_OFFSET), 6: (Constants.WIDTH - self.RIGHT_OFFSET, Constants.HEIGHT // 3), 7: (Constants.WIDTH - self.RIGHT_OFFSET, Constants.HEIGHT // 3 * 2)},
        }
