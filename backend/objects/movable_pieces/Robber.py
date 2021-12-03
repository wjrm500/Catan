class Robber:
    def __init__(self):
        self.hexagon = None
    
    def place_on_hexagon(self, hexagon):
        if self.hexagon is not None:
            self.hexagon.robber = False
        self.hexagon = hexagon
        hexagon.robber = True