class Player:
    def __init__(self, id):
        self.id = id

        self.cards = []

    def __repr__(self):
        return f"<Player {self.id}, {self.cards}>"
