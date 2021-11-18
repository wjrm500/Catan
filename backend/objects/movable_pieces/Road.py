from backend.Incrementable import Incrementable

class Road(Incrementable):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.line = None