from collections import Counter
import random

from frontend.GeneralUtils import GeneralUtils as gutils

class Robber:
    def __init__(self, distributor):
        self.distributor = distributor
        self.hexagon = None
    
    def place_on_hexagon(self, hexagon):
        if self.hexagon is not None:
            self.hexagon.robber = False
        self.hexagon = hexagon
        hexagon.robber = True

    def do_the_robbing(self, robber_mover, from_development_card):
        text_events = []
        if not from_development_card:
            rtr_text_events = self.rob_the_rich()
            text_events.extend(rtr_text_events)
        rap_text_events = self.rob_adjacent_player(robber_mover)
        text_events.extend(rap_text_events)
        return text_events
    
    def rob_the_rich(self):
        ### Bank robs all players with 8 or more resources
        game = self.distributor.game
        for_text_gen = {}
        text_events = []
        for player in game.players:
            for_text_gen[player] = []
            if (num_resources_in_hand := len(player.hand['resource'])) >= 8:
                for _ in range(num_resources_in_hand // 2):
                    random_resource_card = player.hand['resource'].pop(random.randrange(len(player.hand['resource'])))
                    player.resources_lost_to_robber[random_resource_card.type] += 1
                    game.resource_cards[random_resource_card.type].append(random_resource_card)
                    for_text_gen[player].append(random_resource_card.type)
            for_text_gen[player] = dict(Counter(for_text_gen[player]))
        
        for player, resource_counter in for_text_gen.items():
            resources_lost_list = [f'{num_lost} {resource_type}' for resource_type, num_lost in resource_counter.items()]
            if resources_lost_list:
                if len(resources_lost_list) > 1:
                    resources_lost_text = gutils.comma_separate_with_ampersand(resources_lost_list)
                else:
                    resources_lost_text = f'{resources_lost_list[0]}'
                text_event = f'The bank stole {resources_lost_text} from {player.name}!'
                text_events.append(text_event)
        return text_events
    
    def rob_adjacent_player(self, robber_mover):
         ### Active player robs random player with settlement on robbed hexagon
        text_events = []
        settled_nodes = [node for node in self.hexagon.nodes if node.settlement and node.settlement.player is not robber_mover]
        if settled_nodes:
            random_settled_node = random.choice(settled_nodes)
            robbee = random_settled_node.settlement.player
            if len(robbee.hand['resource']) > 0:
                random_resource_card = robbee.hand['resource'].pop(random.randrange(len(robbee.hand['resource'])))
                robber_mover.hand['resource'].append(random_resource_card)
                text_event = f'{robber_mover.name} stole 1 {random_resource_card.type} from {robbee.name}!'
            else:
                text_event = f'{robbee.name} had nothing to steal!'
            text_events.append(text_event)
        return text_events