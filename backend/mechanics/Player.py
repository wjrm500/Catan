from collections import Counter
from actions.ActionFactory import ActionFactory
from backend.Incrementable import Incrementable
from backend.Unserializable import Unserializable
from config import config

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
        if action == ActionFactory.BUILD_ROAD:
            return self.can_afford_build_road()
        elif action == ActionFactory.BUILD_SETTLEMENT:
            return self.can_afford_build_settlement()
    
    ### Can potentially combine can_afford_build_road and can_afford_built_settlement but wait until other methods have been implemented to see what is truly generic
    def can_afford_build_road(self):
        action_config = config['actions'][ActionFactory.BUILD_ROAD]
        resource_card_dict = action_config['cost']['resource_cards']
        return self.has_resource_cards_in_hand(resource_card_dict)
    
    def can_afford_build_settlement(self):
        action_config = config['actions'][ActionFactory.BUILD_SETTLEMENT]
        resource_card_dict = action_config['cost']['resource_cards']
        return self.has_resource_cards_in_hand(resource_card_dict)
    
    def has_resource_cards_in_hand(self, resource_card_dict):
        resource_card_counter = Counter(resource_card_dict)
        hand_counter = Counter([resource_card.type for resource_card in self.hand['resource']])
        hand_counter.subtract(resource_card_counter)
        return len(list(filter(lambda x: x < 0, hand_counter.values()))) == 0
    
    def unserializable_properties(self):
        return ['game']
    
    def num_of_resource_in_hand(self, resource):
        return len([x for x in self.hand['resource'] if x.type == resource])