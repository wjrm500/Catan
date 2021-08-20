import numpy as np
from .Point import Point

class Hexagon:
    def __init__(self, lines, points, resource_type):
        self.lines = lines
        self.points = points
        self.resource_type = resource_type
        for line in self.lines:
            line.hexagons.append(self)
        for point in self.points:
            point.hexagons.append(self)
            if len(point.hexagons) == 3:
                point.on_coast = False
        
    def last_free_point(self):
        for point in self.points[::-1]:
            if len(point.lines) < 3:
                return point
    
    def centre_point(self):
        centre_point_x = np.mean([point.x for point in self.points])
        centre_point_y = np.mean([point.y for point in self.points])
        return (Point(centre_point_x, centre_point_y))