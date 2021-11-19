import math

from backend.Incrementable import Incrementable

class Node(Incrementable):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.hexagons = []
        self.lines = []
        self.on_coast = True
        self.port = None
        self.settlement = None
    
    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return round(self.x, 2) == round(other.x, 2) and round(self.y, 2) == round(other.y, 2)
    
    def start_angle(self):
        if len(self.lines) != 2:
            raise Exception('Starting angle can only be found if node is associated with two lines')
        angle = self.lines[0].angle()
        return angle - math.pi / 3 if angle > math.pi / 2 else angle + math.pi * 5 / 3

    def test(self, x, y):
        return round(self.x, 2) == round(x, 2) and round(self.y, 2) == round(y, 2)
    
    def adjacent_to_settled_node(self):
        for line in self.lines:
            other_node = next(node for node in line.nodes if node is not self)
            if other_node.settlement:
                return True
        return False
    
    def add_settlement(self, settlement):
        self.settlement = settlement
        settlement.node = self
    
    def nominal_value(self):
        return sum(hexagon.num_pips for hexagon in self.hexagons)