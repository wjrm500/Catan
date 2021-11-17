import itertools

class Player:
    new_id = itertools.count()

    def __init__(self, name, client_address):
        self.id = next(Player.new_id)
        self.name = name
        self.client_address = client_address
        self.longest_road = False
        self.largest_army = False
    
    def set_color(self, color):
        self.color = color