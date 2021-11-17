import itertools

from backend.Unserializable import Unserializable

class Player(Unserializable):
    new_id = next(itertools.count())

    def __init__(self, name, client_conn):
        self.id = Player.new_id
        self.name = name
        self.client_conn = client_conn
        self.longest_road = False
        self.largest_army = False
    
    def set_color(self, color):
        self.color = color
    
    def get_address(self):
        return self.client_conn.getpeername()
    
    def unserializable_properties(self):
        return ['client_conn']