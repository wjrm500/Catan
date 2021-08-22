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
        self.resources = self.set_resources()
        self.hexagons = []
        self.distributor = Distributor()
    
    def setup_board(self):
        starting_node = self.distributor.get_node(0, 0)
        hexagon = self.create_hexagon(starting_node, 0)
        while len(self.hexagons) < self.num_hexagons:
            starting_node = hexagon.last_free_node() if len(self.hexagons) > 1 else hexagon.nodes[2]
            starting_angle = starting_node.starting_angle()
            hexagon = self.create_hexagon(starting_node, starting_angle)
        self.assign_ports()

    def create_hexagon(self, node, angle):
        lines, nodes = HexagonDrawing.draw_hexagon(node, angle, self.distributor)
        resource_type = self.get_resource_type()
        hexagon = Hexagon(lines, nodes, resource_type)
        self.hexagons.append(hexagon)
        return hexagon
    
    def set_resources(self):
        resources = []
        resource_types = copy.deepcopy(self.config['resource_types'])
        while len(resources) < self.num_hexagons:
            random_resource_type = random.choices(
                population = [resource_type for resource_type in resource_types.keys()],
                weights = [info['count'] for info in resource_types.values()],
                k = 1
            )[0]
            resources.append(random_resource_type)
            resource_types[random_resource_type]['count'] -= 1
            if sum([info['count'] for info in resource_types.values()]) == 0:
                resource_types = copy.deepcopy(self.config['resource_types'])
        random.shuffle(resources)
        return resources        

    def get_resource_type(self):
        return self.resources.pop()
    
    def assign_ports(self):
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
            iterator += random.randint(2, 4)
            if iterator >= len(coast_nodes) - 1:
                break