from collections import Counter

from backend.Incrementable import Incrementable
from config import config

class Player(Incrementable):
    def __init__(self, game, name, client_address):
        super().__init__()
        self.game = game
        self.name = name
        self.client_address = client_address
        self.army_size = 0
        self.road_length = []
        self.longest_road = 0
        self.hand = {
            'development': [],
            'resource': []
        }
    
    def has_longest_road(self):
        return (road_player := self.game.longest_road['player']) and road_player.id == self.id
    
    def has_largest_army(self):
        return (army_player := self.game.largest_army['player']) and army_player.id == self.id

    def set_longest_road(self):
        ### Credit for the solution goes to kvombatkere @ https://github.com/kvombatkere
        road_lengths = []
        self.build_graph = {}
        self.build_graph['ROADS'] = [(road.line.start_node, road.line.end_node) for road in self.roads if road.line]
        for road in self.build_graph['ROADS']:
            self.road_i_lengths = []
            road_count = 0
            road_arr = []
            vertex_list = []
            self.check_path_length(road, road_arr, road_count, vertex_list)
            road_inverted = (road[1], road[0])
            road_count = 0
            road_arr = []
            vertex_list = []
            self.check_path_length(road_inverted, road_arr, road_count, vertex_list)
            road_lengths.append(max(self.road_i_lengths))
        self.longest_road = max(road_lengths) if road_lengths else 0
        if self.longest_road >= 5 and self.longest_road > self.game.longest_road['road_length']:
            self.game.longest_road = {'player': self, 'road_length': self.longest_road}

    def check_path_length(self, edge, edge_list, road_length, vertex_list):
        edge_list.append(edge)
        road_length += 1
        vertex_list.append(edge[0])
        road_neighbors_list = self.get_neighbouring_roads(edge, edge_list, vertex_list)
        if road_neighbors_list == []:
            self.road_i_lengths.append(road_length)
            return
        else:
            for neighbor_road in road_neighbors_list:
                self.check_path_length(neighbor_road, edge_list, road_length, vertex_list)

    def get_neighbouring_roads(self, road_i, visited_roads, visited_vertices):
        new_neighbours = []
        v1 = road_i[0]
        v2 = road_i[1] 
        for edge in self.build_graph['ROADS']:
            if edge[1] in visited_vertices:
                edge = (edge[1], edge[0])
            if edge not in visited_roads:
                if v2.settlement and v2.settlement.player.id != self.id:
                    continue
                if edge[0] == v2 and edge[0] not in visited_vertices:
                    new_neighbours.append(edge)
                if edge[0] == v1 and edge[0] not in visited_vertices:
                    new_neighbours.append(edge)
                if edge[1] == v2 and edge[1] not in visited_vertices:
                    new_neighbours.append((edge[1], edge[0]))
                if edge[1] == v1 and edge[1] not in visited_vertices:
                    new_neighbours.append((edge[1], edge[0]))
        return new_neighbours

    def victory_points(self):
        from_settlements = sum([(2 if settlement.city else 1) for settlement in self.settlements if settlement.node])
        from_achievements = (2 if self.has_longest_road() else 0) + (2 if self.has_largest_army() else 0)
        from_development_cards = len([card for card in self.hand['development'] if card.type == 'victory_point'])
        return from_settlements + from_achievements + from_development_cards
    
    def set_color(self, color):
        self.color = color
    
    def can_do(self, action):
        if action == 'BUILD_ROAD':
            return self.can_build_road()
        elif action == 'BUILD_SETTLEMENT':
            return self.can_build_settlement()
        elif action == 'BUY_DEVELOPMENT_CARD':
            return self.can_buy_development_card()
        elif action == 'MOVE_ROBBER_TO_DESERT':
            return self.can_move_robber_to_desert()
        elif action == 'SWAP_CARDS':
            return self.can_swap_cards()
        elif action == 'TRADE_WITH_BANK':
            return self.can_trade_with_bank()
        elif action == 'UPGRADE_SETTLEMENT':
            return self.can_upgrade_settlement()
        elif action == 'USE_DEVELOPMENT_CARD':
            return self.can_use_development_card()
    
    def can_build_road(self):
        resource_card_dict = self.get_resource_card_dict('BUILD_ROAD')
        has_resource_cards_in_hand = self.has_resource_cards_in_hand(resource_card_dict)

        ### Check for roadworthy line
        roads_on_board = [x for x in self.roads if x.line] ### Roads that have been placed on board
        nodes_on_roads = [node for road in roads_on_board for node in road.line.nodes if not (node.settlement and node.settlement.player is not self)] ### Lineworthy nodes
        lines_from_roads = [line for node in nodes_on_roads for line in node.lines if not line.road] ### Roadworthy lines extending from roads
        settlements_on_board = [x for x in self.settlements if x.node] ### Settlements that have been placed on board
        lines_from_settlements = [line for settlement in settlements_on_board for line in settlement.node.lines if not line.road] ### Roadworthy lines extending from settlements
        roadworthy_lines = lines_from_roads + lines_from_settlements 
        
        return has_resource_cards_in_hand and self.num_tokens_available('road') > 0 and len(roadworthy_lines) > 0
    
    def can_build_settlement(self):
        resource_card_dict = self.get_resource_card_dict('BUILD_SETTLEMENT')
        has_resource_cards_in_hand = self.has_resource_cards_in_hand(resource_card_dict)

        ### Check for settleworthy node
        roads_on_board = [x for x in self.roads if x.line]
        nodes_on_roads = [node for road in roads_on_board for node in road.line.nodes]
        settleworthy_nodes = [node for node in nodes_on_roads if not node.settlement and not node.adjacent_to_settled_node()]

        return has_resource_cards_in_hand and self.num_tokens_available('settlement') > 0 and len(settleworthy_nodes) > 0
    
    def bank_trade_cost(self, resource_type, port_types = None):
        port_types = port_types or self.port_types()
        if resource_type in port_types:
            return 2
        if 'general' in port_types:
            return 3
        return 4
    
    def port_types(self):
        port_settlements = [settlement for settlement in self.settlements if settlement.node and settlement.node.port]
        return set([settlement.node.port.type for settlement in port_settlements])

    def can_buy_development_card(self):
        resource_card_dict = self.get_resource_card_dict('BUY_DEVELOPMENT_CARD')
        has_resource_cards_in_hand = self.has_resource_cards_in_hand(resource_card_dict)
        return has_resource_cards_in_hand and len(self.game.development_cards) > 0

    def can_trade_with_bank(self):
        port_types = self.port_types()
        resource_nums = dict(Counter([resource_card.type for resource_card in self.hand['resource']]))
        for resource_type, num in resource_nums.items():
            cost = self.bank_trade_cost(resource_type, port_types)
            if num >= cost:
                return True
        return False
    
    def can_upgrade_settlement(self):
        resource_card_dict = self.get_resource_card_dict('UPGRADE_SETTLEMENT')
        has_resource_cards_in_hand = self.has_resource_cards_in_hand(resource_card_dict)
        has_settlement_on_board = len([settlement for settlement in self.settlements if settlement.node and not settlement.city]) > 0
        has_token_available = self.num_tokens_available('city') > 0
        return has_resource_cards_in_hand and has_settlement_on_board and has_token_available

    def can_use_development_card(self):
        return len([card for card in self.hand['development'] if not card.type == 'victory_point']) > 0
    
    def can_move_robber_to_desert(self):
        board_has_desert = len([hexagon for hexagon in self.game.distributor.hexagons if hexagon.resource_type == 'desert']) > 0
        has_token_available = self.num_tokens_available('game') > 0
        return board_has_desert and has_token_available
    
    def can_swap_cards(self):
        has_two_cards_in_hand = len(self.hand['resource']) > 1
        at_least_one_opponent_has_two_cards_in_hand = len([player for player in self.game.players if player.id != self.id and len(player.hand['resource']) > 1]) > 0
        has_token_available = self.num_tokens_available('game') > 0
        return has_two_cards_in_hand and at_least_one_opponent_has_two_cards_in_hand and has_token_available
    
    def has_resource_cards_in_hand(self, resource_card_dict):
        resource_card_counter = Counter(resource_card_dict)
        hand_counter = Counter([resource_card.type for resource_card in self.hand['resource']])
        hand_counter.subtract(resource_card_counter)
        return len(list(filter(lambda x: x < 0, hand_counter.values()))) == 0

    def num_of_card_type_in_hand(self, card_type):
        resource_card_num = len([x for x in self.hand['resource'] if x.type == card_type])
        development_card_num = len([x for x in self.hand['development'] if x.type == card_type])
        return resource_card_num or development_card_num
    
    def get_resource_card_dict(self, action):
        d = {
            'BUILD_ROAD': {'brick': 1, 'lumber': 1},
            'BUILD_SETTLEMENT': {'brick': 1, 'grain': 1, 'lumber': 1, 'wool': 1},
            'BUY_DEVELOPMENT_CARD': {'grain': 1, 'ore': 1, 'wool': 1},
            'UPGRADE_SETTLEMENT': {'grain': 2, 'ore': 3}
        }
        return d[action]
    
    def subtract_and_return_resources_from_hand(self, resource_card_dict):
        marked_for_removal = []
        if self.game.started_proper: ### No need to pay for road in settle phase
            for resource_card in self.hand['resource']:
                if resource_card.type in resource_card_dict:
                    marked_for_removal.append(resource_card)
                    resource_card_dict[resource_card.type] -= 1
                    if resource_card_dict[resource_card.type] == 0:
                        del resource_card_dict[resource_card.type]
            self.hand['resource'] = [resource_card for resource_card in self.hand['resource'] if resource_card not in marked_for_removal]
        return marked_for_removal
    
    def transfer_resources_to_player(self, resource_card_dict, player):
        resource_cards = self.subtract_and_return_resources_from_hand(resource_card_dict)
        player.hand['resource'].extend(resource_cards)
    
    def transfer_resources_to_bank(self, resource_card_dict):
        resource_cards = self.subtract_and_return_resources_from_hand(resource_card_dict)
        for resource_card in resource_cards:
            self.game.resource_cards[resource_card.type].append(resource_card)
    
    def get_free_road(self):
        return next(road for road in self.roads if not road.line)
    
    def get_free_settlement(self):
        return next(settlement for settlement in self.settlements if not settlement.node)
    
    def num_tokens_available(self, type):
        if type == 'road':
            return len([road for road in self.roads if not road.line])
        elif type == 'settlement':
            return len([settlement for settlement in self.settlements if not settlement.node or settlement.city])
        elif type == 'city':
            return len([city for city in self.cities if not city.settlement])
        elif type == 'game':
            return self.num_game_tokens
        
    def pip_dict(self):
        settlements_on_board = [settlement for settlement in self.settlements if settlement.node]
        accessed_hexagons = {hexagon: (2 if settlement.city else 1) for settlement in settlements_on_board for hexagon in settlement.node.hexagons if hexagon.resource_type != 'desert'}
        pip_dict = {resource_type: 0 for resource_type in list(config['resource_types'].keys()) if resource_type != 'desert'}
        for hexagon, multiplier in accessed_hexagons.items():
            pip_dict[hexagon.resource_type] = pip_dict.get(hexagon.resource_type) + (hexagon.num_pips * multiplier)
        return pip_dict