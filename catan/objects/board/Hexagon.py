import numpy as np

class Hexagon:
    def __init__(self, lines, nodes):
        self.lines = lines
        self.nodes = nodes
        self.resource_type = None
        self.roll_num = None
        self.num_pips = 0
        self.robber = False
        for line in self.lines:
            line.hexagons.append(self)
        for node in self.nodes:
            node.hexagons.append(self)
            if len(node.hexagons) == 3:
                node.on_coast = False
    
    def set_resource_type(self, resource_type):
        self.resource_type = resource_type
    
    def set_roll_num(self, roll_num):
        self.roll_num = roll_num
        self.num_pips = 6 - abs(self.roll_num - 7)
        
    def last_free_node(self):
        for node in self.nodes[::-1]:
            if len(node.lines) < 3:
                return node
    
    def centre_point(self):
        centre_point_x = np.mean([node.x for node in self.nodes])
        centre_point_y = np.mean([node.y for node in self.nodes])
        return (centre_point_x, centre_point_y)