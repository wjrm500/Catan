from ..objects.board.Line import Line
from ..objects.board.Node import Node

class Distributor:
    def __init__(self):
        self.lines = []
        self.nodes = []
    
    def get_line(self, start_node, end_node):
        for line in self.lines:
            if line.test(start_node, end_node):
                return line
        line = Line(start_node, end_node)
        self.lines.append(line)
        return line
    
    def get_node(self, x, y):
        for node in self.nodes:
            if node.test(x, y):
                return node
        node = Node(x, y)
        self.nodes.append(node)
        return node