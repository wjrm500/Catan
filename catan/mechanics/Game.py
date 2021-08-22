from .drawing.HexagonDrawing import HexagonDrawing
import random
import copy
from ..objects.board.Hexagon import Hexagon
from ..objects.board.Port import Port
from .Distributor import Distributor

class Game:
    def __init__(self, config, num_hexagons = 19):
        self.config = config
        self.num_hexagons = num_hexagons
        self.hexagons = []
        self.distributor = Distributor()
    
    def setup_board(self):
        start_node = self.distributor.get_node(0, 0)
        hexagon = self.create_hexagon(start_node, 0)
        while len(self.hexagons) < self.num_hexagons:
            start_node = hexagon.last_free_node() if len(self.hexagons) > 1 else hexagon.nodes[2]
            start_angle = start_node.start_angle()
            hexagon = self.create_hexagon(start_node, start_angle)
        self.assign_resource_types_to_hexagons()
        self.assign_ports_to_coast_nodes()

    def create_hexagon(self, node, angle):
        lines, nodes = HexagonDrawing.draw_hexagon(node, angle, self.distributor)
        hexagon = Hexagon(lines, nodes)
        self.hexagons.append(hexagon)
        return hexagon
    
    def assign_resource_types_to_hexagons(self):
        resource_types = copy.deepcopy(self.config['resource_types'])
        for hexagon in self.hexagons:
            random_resource_type = random.choices(
                population = [resource_type for resource_type in resource_types.keys()],
                weights = [info['count'] for info in resource_types.values()],
                k = 1
            )[0]
            hexagon.set_resource_type(random_resource_type)
            resource_types[random_resource_type]['count'] -= 1
            if sum([info['count'] for info in resource_types.values()]) == 0:
                resource_types = copy.deepcopy(self.config['resource_types'])   

    def get_resource_type(self):
        return self.resources.pop()
    
    def assign_ports_to_coast_nodes(self):
        coast_nodes = [node for node in self.distributor.nodes if node.on_coast]
        iterator = 0
        port_types = copy.deepcopy(self.config['port_types'])
        while True:
            random_port_type = random.choices(
                population = [port_type for port_type in port_types.keys()],
                weights = [info['count'] for info in port_types.values()],
                k = 1
            )[0]
            port_types[random_port_type]['count'] -= 1
            coast_nodes[iterator].port = Port(random_port_type)
            if sum([info['count'] for info in port_types.values()]) == 0:
                port_types = copy.deepcopy(self.config['port_types'])
            iterator += random.choices(
                population = [1, 2, 3, 4],
                weights = [0.1, 0.4, 0.4, 0.1],
                k = 1
            )[0]
            if iterator >= len(coast_nodes) - 1:
                break