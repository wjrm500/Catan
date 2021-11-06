class Player:
    def __init__(self, name, client_conn):
        self.name = name
        self.client_conn = client_conn
        self.longest_road = False
        self.largest_army = False
    
    def get_address(self):
        return self.client_conn.getpeername()