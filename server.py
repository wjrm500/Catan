import os
from better_profanity import profanity
from collections import Counter
import random
import socket
import threading

from ClientServerInterface import ClientServerInterface
from actions.ActionFactory import ActionFactory
from backend.mechanics.Distributor import Distributor
from backend.mechanics.Player import Player
from config import config
from backend.mechanics.Game import Game
from frontend.GeneralUtils import GeneralUtils as gutils

class Server:
    # LOCAL_HOST = '127.0.0.1'
    # LOCAL_PORT = 9090
    REMOTE_HOST = ''
    REMOTE_PORT = 9090

    def __init__(self):
        self.interface = ClientServerInterface()
        self.games = {}
        self.host = self.REMOTE_HOST
        self.port = self.REMOTE_PORT
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print(f'Listening for incoming connections at {(self.host, self.port)}')
    
    def serve(self):
        while True:
            client_conn, client_address = self.socket.accept()
            print(f"{str(client_address)} connected")
            thread = threading.Thread(target = self.handle, args = (client_conn,))
            thread.start()
            
    def handle(self, client):
        while True:
            try:
                client_address = client.getpeername()
                input_data = self.interface.receive_data(client)
                print(f'Incoming... Client: {client_address} | Data: {input_data}')
                action = input_data['action']
                if action == ActionFactory.ADD_PLAYER:
                    game_code = input_data['game_code']
                    game = self.games[game_code]
                    player = Player(game, input_data['player'], client_address)
                    game.add_player(player)
                    output_data = {'action': action, 'player': player}
                    self.broadcast_to_game(game.code, output_data)
                elif action == ActionFactory.BUILD_ROAD:
                    game_code = input_data['game_code']
                    game = self.games[game_code]
                    active_player = game.get_player_from_client_address(client_address)
                    line = game.distributor.get_object_by_id(Distributor.OBJ_LINE, input_data['line_id'])
                    if not input_data['from_development_card']:
                        active_player.transfer_resources_to_bank(active_player.get_resource_card_dict(action))
                    else:
                        if input_data['road_building_turn_index'] == 0:
                            card_to_remove = next(card for card in active_player.hand['development'] if card.type == 'road_building')
                            active_player.hand['development'].remove(card_to_remove)
                    line.add_road(road := active_player.get_free_road())
                    active_player.set_longest_road()
                    output_data = {'action': action, 'from_development_card': input_data['from_development_card'], 'line_id': line.id, 'player': active_player, 'players': game.players, 'road_id': road.id, 'road_building_turn_index': input_data['road_building_turn_index']}
                    self.broadcast_to_game(game.code, output_data)
                elif action == ActionFactory.BUILD_VILLAGE:
                    game_code = input_data['game_code']
                    game = self.games[game_code]
                    active_player = game.get_player_from_client_address(client_address)
                    node = game.distributor.get_object_by_id(Distributor.OBJ_NODE, input_data['node_id'])
                    active_player.transfer_resources_to_bank(active_player.get_resource_card_dict(action))
                    node.add_village(village := active_player.get_free_village())
                    if len([line for line in node.lines if line.road]) >= 2: ### Settlement has at least two roads extending from it
                        for player in game.players:
                            player.set_longest_road() ### Settlement might have broken road
                        if game.longest_road['road_length'] < 5:
                            game.longest_road = {'player': None, 'road_length': 0} ### Previous longest road holder may no longer own that title
                    if 'desert' in [hexagon.resource_type for hexagon in node.hexagons] or node.on_coast: ### Return game token if new village on desert hex or coast
                        active_player.num_game_tokens += 1
                    output_data = {'action': action, 'node_id': node.id, 'player': active_player, 'players': game.players, 'village_id': village.id}
                    self.broadcast_to_game(game.code, output_data)
                elif action == ActionFactory.BUY_DEVELOPMENT_CARD:
                    game_code = input_data['game_code']
                    game = self.games[game_code]
                    player = game.get_player_from_client_address(client_address)
                    development_card = game.development_cards.pop()
                    player.hand['development'].append(development_card)
                    player.transfer_resources_to_bank(player.get_resource_card_dict(action))
                    output_data = {'action': action, 'player': player, 'players': game.players}
                    self.broadcast_to_game(game.code, output_data)
                elif action == ActionFactory.CREATE_NEW_GAME:
                    num_hexagons = input_data['num_hexagons']
                    game = Game(config, num_hexagons)
                    game.add_client(client)
                    self.games[game.code] = game
                    output_data = {'action': action, 'game_code': game.code}
                    self.broadcast_to_game(game.code, output_data)
                elif action == ActionFactory.END_TURN:
                    game_code = input_data['game_code']
                    game = self.games[game_code]
                    player = game.get_player_from_client_address(client_address)
                    if player == game.players[-1]:
                        game.rounds_completed += 1
                    self.broadcast_to_game(game.code, {'action': action, 'player': player, 'rounds_completed': game.rounds_completed})
                elif action == ActionFactory.JOIN_EXISTING_GAME:
                    game_code = input_data['game_code']
                    output_data = {'action': action}
                    if game_code in self.games:
                        game = self.games[game_code]
                        game.add_client(client)
                        output_data.update({'game_code': game.code, 'players': game.players})
                        self.broadcast_to_game(game.code, output_data)
                    else:
                        output_data['error'] = f'"{game_code}" is not a valid game code'
                        self.broadcast_to_client(client, output_data)
                elif action == ActionFactory.MOVE_ROBBER_TO_DESERT:
                    game_code = input_data['game_code']
                    game = self.games[game_code]
                    hexagon = next(iter(sorted([hexagon for hexagon in game.distributor.hexagons if hexagon.resource_type == 'desert'], key = lambda x: random.random())))
                    robber = game.distributor.robber
                    robber.place_on_hexagon(hexagon)
                    player = game.get_player_from_client_address(client_address)
                    player.num_game_tokens -= player.game_token_cost()
                    output_data.update({'action': action, 'hexagon_id': hexagon.id, 'player': player, 'players': game.players})
                    self.broadcast_to_game(game.code, output_data)
                elif action == ActionFactory.PLACE_ROBBER:
                    game_code = input_data['game_code']
                    game = self.games[game_code]
                    player = game.get_player_from_client_address(client_address)
                    hexagon = game.distributor.get_object_by_id(Distributor.OBJ_HEXAGON, input_data['hexagon_id'])
                    robber = game.distributor.robber
                    robber.place_on_hexagon(hexagon)
                    from_development_card = input_data['from_development_card']
                    text_events = robber.do_the_robbing(robber_mover = player, from_development_card = from_development_card)
                    if from_development_card:
                        card_to_remove = next(card for card in player.hand['development'] if card.type == 'knight')
                        player.hand['development'].remove(card_to_remove)
                        player.army_size += 1
                        if player.army_size >= 3 and player.army_size > game.largest_army['army_size']:
                            game.largest_army = {'player': player, 'army_size': player.army_size}
                    output_data = {'action': action, 'from_development_card': from_development_card, 'hexagon_id': hexagon.id, 'player': player, 'players': game.players, 'text_events': text_events}
                    self.broadcast_to_game(game_code, output_data)
                elif action == ActionFactory.PLAY_MONOPOLY_CARD:
                    game_code = input_data['game_code']
                    game = self.games[game_code]
                    active_player = game.get_player_from_client_address(client_address)
                    resource_type = input_data['resource_type']
                    num_received = 0
                    for other_player in game.players:
                        if other_player == active_player: continue
                        other_player.hand['resource'], cards_to_give = gutils.filter_list(other_player.hand['resource'], lambda card: card.type != resource_type)
                        active_player.hand['resource'].extend(cards_to_give)
                        num_received += len(cards_to_give)
                    card_to_remove = next(card for card in active_player.hand['development'] if card.type == 'monopoly')
                    active_player.hand['development'].remove(card_to_remove)
                    output_data = {'action': action, 'num_received': num_received, 'player': active_player, 'players': game.players, 'resource_type': resource_type}
                    self.broadcast_to_game(game_code, output_data)
                elif action == ActionFactory.PLAY_YEAR_OF_PLENTY_CARD:
                    game_code = input_data['game_code']
                    game = self.games[game_code]
                    player = game.get_player_from_client_address(client_address)
                    year_of_plenty_turn_index = input_data['year_of_plenty_turn_index']
                    cards_of_type = game.resource_cards[input_data['resource_type']]
                    bank_unable_to_pay = False
                    if len(cards_of_type) > 0:
                        resource_card = cards_of_type.pop()
                        player.hand['resource'].append(resource_card)
                        if year_of_plenty_turn_index == 0:
                            card_to_remove = next(card for card in player.hand['development'] if card.type == 'year_of_plenty')
                            player.hand['development'].remove(card_to_remove)
                    else:
                        bank_unable_to_pay = True
                    output_data = {'action': action, 'bank_unable_to_pay': bank_unable_to_pay, 'player': player, 'players': game.players, 'resource_type': input_data['resource_type'], 'year_of_plenty_turn_index': input_data['year_of_plenty_turn_index']}
                    self.broadcast_to_game(game_code, output_data)
                elif action == ActionFactory.ROLL_DICE:
                    game_code = input_data['game_code']
                    game = self.games[game_code]
                    player = game.get_player_from_client_address(client_address)
                    dice_roll = game.roll_dice()
                    output_data = {'action': action, 'dice_roll': dice_roll, 'player': player, 'players': game.players}
                    self.broadcast_to_game(game_code, output_data)
                elif action == ActionFactory.SEND_CHAT_MESSAGE:
                    game_code = input_data['game_code']
                    game = self.games[game_code]
                    player = game.get_player_from_client_address(client_address)
                    message = profanity.censor(input_data['message'])
                    output_data = {'action': action, 'message': message, 'player': player, 'players': game.players}
                    self.broadcast_to_game(game_code, output_data)
                elif action == ActionFactory.START_GAME:
                    game_code = input_data['game_code']
                    game = self.games[game_code]
                    game.setup_board()
                    game.setup_cards()
                    game.setup_movable_pieces()
                    game.randomise_player_order_and_assign_colors()
                    game.started = True
                    self.broadcast_to_game(game.code, {'action': action, 'distributor': game.distributor, 'players': game.players})
                elif action == ActionFactory.START_GAME_PROPER:
                    game_code = input_data['game_code']
                    game = self.games[game_code]
                    game.started_proper = True
                    self.broadcast_to_game(input_data['game_code'], {'action': action})
                elif action == ActionFactory.SWAP_CARDS:
                    game_code = input_data['game_code']
                    game = self.games[game_code]
                    active_player = game.get_player_from_client_address(client_address)
                    random_opponent = random.choice([player for player in game.players if player is not active_player and len(player.hand['resource']) > 1]) ### With at least two cards in hand
                    reverse_swap_resource_types = sorted([resource_card.type for resource_card in random_opponent.hand['resource']], key = lambda x: random.random())[:2]
                    receive_resource_card_dict = dict(Counter(reverse_swap_resource_types))
                    random_opponent.transfer_resources_to_player(receive_resource_card_dict.copy(), active_player) ### Random opponent must transfer before active player to prevent possibility of sending same cards back
                    swap_card_resource_types = input_data['swap_card_resource_types']
                    give_resource_card_dict = dict(Counter(swap_card_resource_types))
                    active_player.transfer_resources_to_player(give_resource_card_dict.copy(), random_opponent)
                    active_player.num_game_tokens -= 1
                    output_data = {'action': action, 'give_resource_card_dict': give_resource_card_dict, 'player': active_player, 'players': game.players, 'random_opponent': random_opponent, 'receive_resource_card_dict': receive_resource_card_dict}
                    self.broadcast_to_game(game_code, output_data)
                elif action == ActionFactory.TRADE_WITH_BANK:
                    game_code = input_data['game_code']
                    game = self.games[game_code]
                    player = game.get_player_from_client_address(client_address)
                    give_type = input_data['give_type']
                    cost = player.bank_trade_cost(give_type)
                    player.transfer_resources_to_bank({give_type: cost})
                    resource_card = game.resource_cards[input_data['receive_type']].pop()
                    player.hand['resource'].append(resource_card)
                    history_text = f'\n\n{player.name} traded {cost} {give_type} to the bank and received 1 {input_data["receive_type"]} in return.'
                    output_data = {'action': action, 'history_text': history_text, 'player': player}
                    self.broadcast_to_game(game_code, output_data)
                elif action == ActionFactory.UPGRADE_SETTLEMENT:
                    game_code = input_data['game_code']
                    game = self.games[game_code]
                    player = game.get_player_from_client_address(client_address)
                    node = game.distributor.get_object_by_id(Distributor.OBJ_NODE, input_data['node_id'])
                    player.transfer_resources_to_bank(player.get_resource_card_dict(action))
                    node.add_city(city := active_player.get_free_city())
                    output_data = {'action': action, 'city_id': city.id, 'node_id': node.id, 'player': player, 'players': game.players}
                    self.broadcast_to_game(game_code, output_data)
            except Exception as e:
                print(str(e))
                ### End any games for which the client was the main client
                game_codes_to_delete = []
                for game_code, game in self.games.items():
                    if game.main_client == client:
                        game.delete_client_and_corresponding_player_if_applicable(client_address)
                        self.broadcast_to_game(game.code, {'action': ActionFactory.END_GAME})
                        game_codes_to_delete.append(game_code)

                ### If game started, end any games involving the client
                ### If game not yet started, simply remove client from game
                for game_code, game in self.games.items():
                    if client_address in game.clients:
                        player = game.get_player_from_client_address(client_address)
                        game.delete_client_and_corresponding_player_if_applicable(client_address)
                        if game.started:
                            self.broadcast_to_game(game.code, {'action': ActionFactory.END_GAME})
                            game_codes_to_delete.append(game_code)
                        else:
                            self.broadcast_to_game(game_code, {'action': ActionFactory.REMOVE_PLAYER, 'player': player})

                for game_code in game_codes_to_delete:
                    del self.games[game_code]

                client.shutdown(2)
                client.close()
                break
        
    def broadcast_to_client(self, client, message):
        self.interface.send_data(client, message)
        print(f'Outgoing... {message}')
    
    def broadcast_to_game(self, game_code, message):
        for client in self.games[game_code].clients.values():
            self.broadcast_to_client(client, message)

server = Server()
server.serve()