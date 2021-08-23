from .drawing.HexagonDrawing import HexagonDrawing
import random
import copy
from ..objects.board.Port import Port
from .Distributor import Distributor
from ..objects.cards.ResourceCard import ResourceCard
from .Player import Player
from ..objects.movable_pieces.City import City
from ..objects.movable_pieces.Road import Road
from ..objects.movable_pieces.Settlement import Settlement

class Game:
    def __init__(self, config, player_names, num_hexagons = 19):
        self.config = config
        self.num_hexagons = num_hexagons
        self.players = [Player(player_name) for player_name in player_names]
        self.hexagons = []
        self.distributor = Distributor()
    
    def setup_board(self):
        self.hexagons = HexagonDrawing.draw_hexagons(self)
        self.assign_resource_types_to_hexagons()
        self.assign_roll_nums_to_hexagons()
        self.assign_ports_to_coast_nodes()
    
    def setup_cards(self):
        self.resource_cards = {
            resource_type: [
                ResourceCard(resource_type) for _ in range(self.num_hexagons)
            ] for resource_type in self.config['resource_types'].keys()
            if resource_type != 'desert'
        }
        self.development_cards = []
        development_card_type_counts = copy.deepcopy(self.config['development_card_type_counts'])
        for _ in range(round(self.num_hexagons * 25 / 19)):
            development_card_type = random.choices(
                population = [development_card_type for development_card_type in development_card_type_counts.keys()],
                weights = [count for count in development_card_type_counts.values()],
                k = 1
            )[0]
            development_card = self.distributor.get_development_card(development_card_type)
            self.development_cards.append(development_card)
            development_card_type_counts[development_card_type] -= 1
            if sum(development_card_type_counts.values()) == 0:
                development_card_type_counts = copy.deepcopy(self.config['development_card_type_counts']) 
    
    def setup_movable_pieces(self):
        for player in self.players:
            player.cities = [City() for _ in range(round(self.num_hexagons * 4 / 19))]
            player.roads = [Road() for _ in range(round(self.num_hexagons * 15 / 19))]
            player.settlements = [Settlement() for _ in range(round(self.num_hexagons * 5 / 19))]

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
    
    def assign_roll_nums_to_hexagons(self):
        roll_num_counts = copy.deepcopy(self.config['roll_num_counts'])
        for hexagon in self.hexagons:
            if hexagon.resource_type == 'desert':
                continue
            random_roll_num = random.choices(
                population = [roll_num for roll_num in roll_num_counts.keys()],
                weights = [count for count in roll_num_counts.values()],
                k = 1
            )[0]
            hexagon.set_roll_num(random_roll_num)
            roll_num_counts[random_roll_num] -= 1
            if sum(roll_num_counts.values()) == 0:
                roll_num_counts = copy.deepcopy(self.config['roll_num_counts']) 

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