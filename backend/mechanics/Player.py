from backend.Incrementable import Incrementable

class Player(Incrementable):
    def __init__(self, name, client_address):
        super().__init__()
        self.name = name
        self.client_address = client_address
        self.longest_road = False
        self.largest_army = False
    
    def set_color(self, color):
        self.color = color