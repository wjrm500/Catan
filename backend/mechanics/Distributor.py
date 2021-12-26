from backend.objects.board.Port import Port
from backend.objects.movable_pieces.City import City
from backend.objects.movable_pieces.Road import Road
from backend.objects.movable_pieces.Robber import Robber
from backend.objects.movable_pieces.Village import Village
from ..objects.board.Hexagon import Hexagon
from ..objects.board.Line import Line
from ..objects.board.Node import Node
from backend.objects.cards.development.Knight import Knight
from backend.objects.cards.development.Monopoly import Monopoly
from backend.objects.cards.development.RoadBuilding import RoadBuilding
from backend.objects.cards.development.VictoryPoint import VictoryPoint
from backend.objects.cards.development.YearOfPlenty import YearOfPlenty

class Distributor:
    OBJ_CITY = 'city'
    OBJ_HEXAGON = 'hexagon'
    OBJ_LINE = 'line'
    OBJ_NODE = 'node'
    OBJ_PORT = 'port'
    OBJ_ROAD = 'road'
    OBJ_VILLAGE = 'village'

    def __init__(self, game):
        self.game = game
        self.cities = []
        self.hexagons = []
        self.lines = []
        self.nodes = []
        self.ports = []
        self.roads = []
        self.villages = []
        self.robber = Robber(self)
    
    def get_city(self, player):
        city = City(player)
        self.cities.append(city)
        return city
    
    def get_hexagon(self, nodes, lines):
        hexagon = Hexagon(nodes, lines)
        self.hexagons.append(hexagon) ### TODO: Fix related issue (try commenting out this line)
        return hexagon
    
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
    
    def get_port(self):
        port = Port()
        self.ports.append(port)
        return port
    
    def get_road(self, player):
        road = Road(player)
        self.roads.append(road)
        return road
    
    def get_village(self, player):
        village = Village(player)
        self.villages.append(village)
        return village
    
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
        if obj == self.OBJ_CITY:
            return next(city for city in self.cities if city.id == id)
        elif obj == self.OBJ_HEXAGON:
            return next(hexagon for hexagon in self.hexagons if hexagon.id == id)
        elif obj == self.OBJ_LINE:
             return next(line for line in self.lines if line.id == id)
        elif obj == self.OBJ_NODE:
            return next(node for node in self.nodes if node.id == id)
        elif obj == self.OBJ_PORT:
            return next(port for port in self.ports if port.id == id)
        elif obj == self.OBJ_ROAD:
            return next(road for road in self.roads if road.id == id)
        elif obj == self.OBJ_VILLAGE:
            return next(village for village in self.villages if village.id == id)