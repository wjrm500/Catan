from collections import Counter
from backend.Incrementable import Incrementable

class Player(Incrementable):
    def __init__(self, game, name, client_address):
        super().__init__()
        self.game = game
        self.name = name
        self.client_address = client_address
        self.army_size = 0
        self.longest_road = False
        self.largest_army = False
        self.hand = {
            'development': [],
            'resource': []
        }
    
    def set_color(self, color):
        self.color = color
    
    def can_do(self, action):
        if action == 'BUILD_ROAD':
            return self.can_build_road()
        elif action == 'BUILD_SETTLEMENT':
            return self.can_build_settlement()
        elif action == 'TRADE_WITH_BANK':
            return self.can_trade_with_bank()
        elif action == 'BUY_DEVELOPMENT_CARD':
            return self.can_buy_development_card()
        elif action == 'UPGRADE_SETTLEMENT':
            return self.can_upgrade_settlement()
        elif action == 'USE_DEVELOPMENT_CARD':
            return self.can_use_development_card()
    
    def can_build_road(self):
        resource_card_dict = self.get_resource_card_dict('BUILD_ROAD')
        has_resource_cards_in_hand = self.has_resource_cards_in_hand(resource_card_dict)

        ### Check for roadworthy line
        roads_on_board = [x for x in self.roads if x.line]
        nodes_on_roads = [node for road in roads_on_board for node in road.line.nodes if not (node.settlement and node.settlement.player is not self)]
        lines_from_nodes = [line for node in nodes_on_roads for line in node.lines]
        roadworthy_lines = [line for line in lines_from_nodes if not line.road]
        
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
        has_settlement_on_board = len([settlement for settlement in self.settlements if settlement.node]) > 0
        has_token_available = self.num_tokens_available('city') > 0
        return has_resource_cards_in_hand and has_settlement_on_board and has_token_available

    def can_use_development_card(self):
        return len([card for card in self.hand['development'] if not card.type == 'victory_point']) > 0
    
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
    
    def transfer_resources_to_bank(self, resource_card_dict):
        if self.game.started_proper: ### No need to pay for road in settle phase
            marked_for_removal = []
            for resource_card in self.hand['resource']:
                if resource_card.type in resource_card_dict:
                    marked_for_removal.append(resource_card)
                    resource_card_dict[resource_card.type] -= 1
                    if resource_card_dict[resource_card.type] == 0:
                        del resource_card_dict[resource_card.type]
                    self.game.resource_cards[resource_card.type].append(resource_card)
            self.hand['resource'] = [resource_card for resource_card in self.hand['resource'] if resource_card not in marked_for_removal]
    
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
            ### TODO: Implement
            return