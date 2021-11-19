import copy
import random
import string

from .Distributor import Distributor
from .drawing.HexagonDrawing import HexagonDrawing
from ..objects.board.Port import Port
from ..objects.cards.ResourceCard import ResourceCard
from ..objects.movable_pieces.City import City
from ..objects.movable_pieces.Road import Road
from ..objects.movable_pieces.Settlement import Settlement

class Game:
    def __init__(self, config, num_hexagons = 19):
        self.config = config
        self.num_hexagons = num_hexagons
        self.clients = {}
        self.players = []
        self.distributor = Distributor()
        self.started = False
        self.code = ''.join(random.choices(string.ascii_lowercase, k = 5))
    
    def add_client(self, client):
        if len(self.clients) == 0:
            self.main_client = client
        self.clients[client.getpeername()] = client
    
    def delete_client_and_corresponding_player_if_applicable(self, client_address):
        player = self.get_player_from_client_address(client_address)
        if player is not None:
            self.players.remove(player)
        del self.clients[client_address]

    def add_player(self, player):
        self.players.append(player)

    def get_player_from_client_address(self, client_address):
        return next((player for player in self.players if player.client_address == client_address), None)
    
    def setup_board(self):
        HexagonDrawing.draw_hexagons(self)
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
            player.cities = [self.distributor.get_city(player) for _ in range(round(self.num_hexagons * 4 / 19))]
            player.roads = [self.distributor.get_road(player) for _ in range(round(self.num_hexagons * 15 / 19))]
            # player.settlements = [self.distributor.get_settlement(player) for _ in range(round(self.num_hexagons * 5 / 19))]
            player.settlements = [self.distributor.get_settlement(player) for _ in range(round(self.num_hexagons * 50 / 19))] ### TODO: Revert to line above - this one for testing

    def assign_resource_types_to_hexagons(self):
        resource_types = copy.deepcopy(self.config['resource_types'])
        for hexagon in self.distributor.hexagons:
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
        for hexagon in self.distributor.hexagons:
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
    
    def randomise_player_order_and_assign_colors(self):
        random.shuffle(self.players)
        for player, color in zip(self.players, self.config['player_colors']):
            player.set_color(color)