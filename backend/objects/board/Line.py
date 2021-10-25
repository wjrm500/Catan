import math
import numpy as np

class Line:
    def __init__(self, line_id, start_node, end_node):
        self.id = line_id
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
    
    def centre_point(self, real = False):
        centre_point_x = np.mean((self.start_node.real_x, self.end_node.real_x) if real else (self.start_node.x, self.end_node.x))
        centre_point_y = np.mean((self.start_node.real_y, self.end_node.real_y) if real else (self.start_node.y, self.end_node.y))
        return (centre_point_x, centre_point_y)