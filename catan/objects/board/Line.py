import math

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
        return self.start_node == start_node and self.end_node == end_node