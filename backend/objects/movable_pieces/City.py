from backend.Incrementable import Incrementable

class City(Incrementable):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.settlement = None