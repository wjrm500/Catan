from ..objects.board.Hexagon import Hexagon
from ..objects.board.Line import Line
from ..objects.board.Node import Node
from backend.objects.cards.development.Knight import Knight
from backend.objects.cards.development.Monopoly import Monopoly
from backend.objects.cards.development.RoadBuilding import RoadBuilding
from backend.objects.cards.development.VictoryPoint import VictoryPoint
from backend.objects.cards.development.YearOfPlenty import YearOfPlenty

class Distributor:
    OBJ_HEXAGON = 'hexagon'
    OBJ_LINE = 'line'
    OBJ_NODE = 'node'

    def __init__(self):
        self.hexagons = []
        self.lines = []
        self.nodes = []
    
    def get_line(self, start_node, end_node):
        for line in self.lines:
            if line.test(start_node, end_node):
                return line
        line = Line(len(self.lines) + 1, start_node, end_node)
        self.lines.append(line)
        return line
    
    def get_node(self, x, y):
        for node in self.nodes:
            if node.test(x, y):
                return node
        node = Node(len(self.nodes) + 1, x, y)
        self.nodes.append(node)
        return node
    
    def get_hexagon(self, nodes, lines):
        return Hexagon(len(self.hexagons) + 1, nodes, lines)
    
    def get_development_card(self, type):
        type_class_mapping = {
            'knight': Knight,
            'monopoly': Monopoly,
            'road_building': RoadBuilding,
            'victory_point': VictoryPoint,
            'year_of_plenty': YearOfPlenty
        }
        return type_class_mapping[type]()
    
    def get_object_by_id(self, obj, id):
        if obj == self.OBJ_HEXAGON:
            return next(hexagon for hexagon in self.hexagon if hexagon.id == id)
        elif obj == self.OBJ_LINE:
             return next(line for line in self.line if line.id == id)
        elif obj == self.OBJ_NODE:
            return next(node for node in self.nodes if node.id == id)