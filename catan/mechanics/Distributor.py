from catan.objects.cards.development.YearOfPlenty import YearOfPlenty
from catan.objects.cards.development.VictoryPoint import VictoryPoint
from catan.objects.cards.development.RoadBuilding import RoadBuilding
from catan.objects.cards.development.Monopoly import Monopoly
from catan.objects.cards.development.Knight import Knight
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
    
    def get_development_card(self, type):
        type_class_mapping = {
            'knight': Knight,
            'monopoly': Monopoly,
            'road_building': RoadBuilding,
            'victory_point': VictoryPoint,
            'year_of_plenty': YearOfPlenty
        }
        return type_class_mapping[type]()