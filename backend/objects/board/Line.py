from collections import namedtuple
import math
import numpy as np

from backend.Incrementable import Incrementable

class Line(Incrementable):
    def __init__(self, start_node, end_node):
        super().__init__()
        self.start_node = start_node
        self.end_node = end_node
        self.nodes = [self.start_node, self.end_node]
        for node in self.nodes:
            node.lines.append(self)
        self.hexagons = []
    
    def angle(self):
        y_change = self.end_node.y - self.start_node.y
        x_change = self.end_node.x - self.start_node.x
        angle = math.atan2(y_change, x_change)
        if angle > math.pi / 2:
            angle = math.pi * 5 / 2 - angle
        elif angle > 0:
            angle = math.pi / 2 - angle
        else:
            angle = math.pi / 2 + abs(angle)
        return angle

    def test(self, start_node, end_node):
        # return self.start_node.test(start_node.x, start_node.y) and self.end_node.test(end_node.x, end_node.y)
        return (self.start_node is start_node and self.end_node is end_node) or (self.start_node is end_node and self.end_node is start_node)
    
    def centre_point(self):
        centre_point_x = np.mean(self.start_node.x, self.end_node.x)
        centre_point_y = np.mean(self.start_node.y, self.end_node.y)
        CentrePoint = namedtuple('CentrePoint', ['x', 'y'])
        return CentrePoint(x = centre_point_x, y = centre_point_y)