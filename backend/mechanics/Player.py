from collections import Counter
from backend.Incrementable import Incrementable
from backend.Unserializable import Unserializable

class Player(Incrementable, Unserializable):
    def __init__(self, game, name, client_address):
        super().__init__()
        self.game = game ### Only available server-side
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
    
    def can_afford(self, action):
        if action == 'BUILD_ROAD':
            return self.can_afford_build_road()
        elif action == 'BUILD_SETTLEMENT':
            return self.can_afford_build_settlement()
        elif action == 'TRADE_WITH_BANK':
            return self.can_afford_trade_with_bank()
    
    def can_afford_build_road(self):
        resource_card_dict = self.get_resource_card_dict('BUILD_ROAD')
        has_resource_cards_in_hand = self.has_resource_cards_in_hand(resource_card_dict)
        return has_resource_cards_in_hand and len(self.roads) > 0
    
    def can_afford_build_settlement(self):
        resource_card_dict = self.get_resource_card_dict('BUILD_SETTLEMENT')
        has_resource_cards_in_hand = self.has_resource_cards_in_hand(resource_card_dict)
        return has_resource_cards_in_hand and len(self.settlements) > 0
    
    def can_afford_trade_with_bank(self):
        port_settlements = [settlement for settlement in self.settlements if settlement.node and settlement.node.port]
        port_types = set([settlement.port.type for settlement in port_settlements])
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
    
    def unserializable_properties(self):
        return ['game']
    
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