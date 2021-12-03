from collections import Counter
from backend.Incrementable import Incrementable

class Player(Incrementable):
    def __init__(self, game, name, client_address):
        super().__init__()
        self.game = game
        self.name = name
        self.client_address = client_address
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
    
    def can_trade_with_bank(self):
        port_settlements = [settlement for settlement in self.settlements if settlement.node and settlement.node.port]
        port_types = set([settlement.node.port.type for settlement in port_settlements])
        resources = dict(Counter([resource_card.type for resource_card in self.hand['resource']]))
        if resources:
            for port_type in port_types:
                if resources.get(port_type, 0) >= 2:
                    return True
            if 'general' in port_types:
                if max(resources.values()) >= 3:
                    return True
            if max(resources.values()) >= 4:
                return True
        return False
    
    def has_resource_cards_in_hand(self, resource_card_dict):
        resource_card_counter = Counter(resource_card_dict)
        hand_counter = Counter([resource_card.type for resource_card in self.hand['resource']])
        hand_counter.subtract(resource_card_counter)
        return len(list(filter(lambda x: x < 0, hand_counter.values()))) == 0

    def num_of_resource_in_hand(self, resource):
        return len([x for x in self.hand['resource'] if x.type == resource])
    
    def get_resource_card_dict(self, action):
        d = {
            'BUILD_ROAD': {'brick': 1, 'lumber': 1},
            'BUILD_SETTLEMENT': {'brick': 1, 'grain': 1, 'lumber': 1, 'wool': 1}
        }
        return d[action]
    
    def subtract_resource_cards_from_hand(self, action):
        resource_card_dict = self.get_resource_card_dict(action)
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