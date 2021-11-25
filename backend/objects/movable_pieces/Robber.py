class Robber:
    def __init__(self):
        self.hexagon = None
    
    def place_on_hexagon(self, hexagon):
        self.hexagon = hexagon
        hexagon.robber = True
        ### Additional stealing logic?