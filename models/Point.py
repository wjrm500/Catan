import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hexagons = []
        self.lines = []
        self.on_coast = True
        self.port_type = None
    
    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return round(self.x, 2) == round(other.x, 2) and round(self.y, 2) == round(other.y, 2)
    
    def starting_angle(self):
        if len(self.lines) != 2:
            raise Exception('Starting angle can only be found if point is associated with two lines')
        angle = self.lines[0].angle()
        return angle - math.pi / 3 if angle > math.pi / 2 else angle + math.pi * 5 / 3

    def test(self, x, y):
        return round(self.x, 2) == round(x, 2) and round(self.y, 2) == round(y, 2)