import math

class Line:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
        self.points = [self.start_point, self.end_point]
        for point in self.points:
            point.lines.append(self)
        self.hexagons = []
    
    def angle(self):
        y_change = self.end_point.y - self.start_point.y
        x_change = self.end_point.x - self.start_point.x
        angle = math.atan2(y_change, x_change)
        if angle > math.pi / 2:
            angle = math.pi * 5 / 2 - angle
        elif angle > 0:
            angle = math.pi / 2 - angle
        else:
            angle = math.pi / 2 + abs(angle)
        return angle

    def test(self, start_point, end_point):
        return self.start_point == start_point and self.end_point == end_point