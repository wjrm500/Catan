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
        if action not in [ActionFactory.BUILD_ROAD, ActionFactory.BUILD_SETTLEMENT]:
            return ### Just temporary
        action_config = config['actions'][action]
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
    
    def pay_for_action(self, action):
        if self.game.started_proper: ### No need to pay for road in settle phase
            if not self.can_afford(action):
                raise Exception
            action_config = config['actions'][action]
            resource_card_dict = action_config['cost']['resource_cards'].copy()
            marked_for_removal = []
            for resource_card in self.hand['resource']:
                if resource_card.type in resource_card_dict:
                    marked_for_removal.append(resource_card)
                    resource_card_dict[resource_card.type] -= 1
                    if resource_card_dict[resource_card.type] == 0:
                        del resource_card_dict[resource_card.type]
                    self.game.resource_cards[resource_card.type].append(resource_card)
            self.hand['resource'] = [resource_card for resource_card in self.hand['resource'] if resource_card not in marked_for_removal]