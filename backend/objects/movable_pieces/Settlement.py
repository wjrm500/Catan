from backend.Incrementable import Incrementable

class Settlement(Incrementable):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.node = None
        self.city = None
    
    def add_city(self, city):
        self.city = city
        city.settlement = self