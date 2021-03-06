from collections import namedtuple
import copy
import random
import string

from backend.mechanics.Distributor import Distributor
from backend.mechanics.drawing.HexagonDrawing import HexagonDrawing
from backend.objects.board.Port import Port
from backend.objects.cards.ResourceCard import ResourceCard
from backend.Unserializable import Unserializable

DiceRoll = namedtuple('DiceRoll', ['roll_1', 'roll_2', 'total', 'text_events', 'proceed_to_action_selection'])

class Game(Unserializable):
    def __init__(self, config, num_hexagons = 19):
        self.config = config
        self.num_hexagons = num_hexagons
        self.clients = {}
        self.players = []
        self.distributor = Distributor(self)
        self.started = False
        self.started_proper = False
        self.code = ''.join(random.choices(string.ascii_lowercase, k = 5))
        self.dice_rolls = []
        self.longest_road = {'player': None, 'road_length': 0}
        self.largest_army = {'player': None, 'army_size': 0}
        self.victory_point_limit = max(8, round(self.num_hexagons * 10 / 19))
        self.rounds_completed = 0
    
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
        self.place_robber_on_desert_hex()
    
    def setup_cards(self):
        self.resource_cards = {
            resource_type: [
                ResourceCard(resource_type) for _ in range(self.num_hexagons)
            ] for resource_type in self.config['resource_types'].keys()
            if resource_type != 'desert'
        }
        self.development_cards = []
        development_card_types = copy.deepcopy(self.config['development_card_types'])
        for _ in range(round(self.num_hexagons * 25 / 19)):
            development_card_type = random.choices(
                population = [development_card_type for development_card_type in development_card_types.keys()],
                weights = [data['count'] for data in development_card_types.values()],
                k = 1
            )[0]
            development_card = self.distributor.get_development_card(development_card_type)
            self.development_cards.append(development_card)
            development_card_types[development_card_type]['count'] -= 1
            if sum(x['count'] for x in development_card_types.values()) == 0:
                development_card_types = copy.deepcopy(self.config['development_card_types']) 
    
    def setup_movable_pieces(self):
        for player in self.players:
            player.cities = [self.distributor.get_city(player) for _ in range(round(self.num_hexagons * 4 / 19))]
            player.roads = [self.distributor.get_road(player) for _ in range(round(max(2, self.num_hexagons * 15 / 19)))]
            player.villages = [self.distributor.get_village(player) for _ in range(max(2, round(self.num_hexagons * 5 / 19)))]
            player.num_game_tokens = round(self.num_hexagons * 5 / 19)
            player.settlements = player.villages + player.cities

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
        
    def place_robber_on_desert_hex(self):
        desert_hexes = [hexagon for hexagon in self.distributor.hexagons if hexagon.resource_type == 'desert'] ### There may be more than one desert hex on larger boards
        if desert_hexes:
            desert_hex = random.choice(desert_hexes)
            self.distributor.robber.place_on_hexagon(desert_hex)
    
    def randomise_player_order_and_assign_colors(self):
        random.shuffle(self.players)
        for player, color in zip(self.players, self.config['player_colors'].keys()):
            player.set_color(color)
        
    def roll_dice(self):
        while True:
            dice_roll_1 = random.randint(1, 6)
            dice_roll_2 = random.randint(1, 6)
            total = dice_roll_1 + dice_roll_2
            if len(self.dice_rolls) % 2 != 0 and self.dice_rolls[-1] == total: ### Same turn, same number
                continue
            break
        self.dice_rolls.append(total)
        text_events = []
        bounties_gained = {
            player: {resource_type: {'won': 0, 'robbed': 0} for resource_type in self.config['resource_types'].keys()}
            for player in self.players
        }
        for hexagon in self.distributor.hexagons:
            if total == hexagon.roll_num:
                ### Look ahead to make sure the bank has enough resource cards to pay out full bounty to all players
                bounty_from_node = lambda node: node.settlement.victory_points if node.settlement else 0
                total_bounty = sum(bounty_from_node(node) for node in hexagon.nodes)
                if total_bounty > len(resource_cards := self.resource_cards[hexagon.resource_type]):
                    text_event = f"The bank doesn't have enough {hexagon.resource_type} cards to pay out a bounty!"
                    text_events.append(text_event)
                    break
                
                for node in hexagon.nodes:
                    if (settlement := node.settlement):
                        player = settlement.player
                        bounty = settlement.victory_points
                        bounties_gained[player][hexagon.resource_type]['won'] += bounty
                        player.resources_won[hexagon.resource_type] += bounty
                        if not hexagon.robber:
                            for _ in range(bounty):
                                resource_card = resource_cards.pop()
                                player.hand['resource'].append(resource_card)
                        else:
                            bounties_gained[player][hexagon.resource_type]['robbed'] += bounty
                            player.resources_lost_to_robber[hexagon.resource_type] += bounty
                            
        for player, v1 in bounties_gained.items():
            for resource_type, v2 in v1.items():
                num_won, num_robbed = v2['won'], v2['robbed']
                if num_won > 0:
                    text_event = f'{player.name} gained {num_won} {resource_type}'
                    if num_robbed > 0:
                        if num_won == num_robbed:
                            if num_robbed == 1:
                                text_event += '... but the robber stole it!'
                            else: 
                                text_event += '... but the robber stole it all!'
                        else:
                            text_event += f'... but the robber stole {num_robbed}!'
                    else:
                        text_event += '!'
                    text_events.append(text_event)

        if not text_events:
            text_events = ['Nobody gained anything.']
        proceed_to_action_selection = len(self.dice_rolls) % 2 == 0 ### If total dice rolls is even after this dice roll then it's time for the active player to proceed to action selection
        return DiceRoll(dice_roll_1, dice_roll_2, total, text_events, proceed_to_action_selection)
    
    def unserializable_properties(self):
        return ['clients', 'main_client']