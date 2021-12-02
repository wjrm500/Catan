import random
import socket
import threading

from ClientServerInterface import ClientServerInterface
from actions.ActionFactory import ActionFactory
from backend.mechanics.Distributor import Distributor
from backend.mechanics.Player import Player
from config import config
from backend.mechanics.Game import Game

class Server:
    LOCAL_HOST = '127.0.0.1'
    LOCAL_PORT = 9090

    def __init__(self):
        self.interface = ClientServerInterface()
        self.games = {}
        self.host = self.LOCAL_HOST
        self.port = self.LOCAL_PORT
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
                    player = game.get_player_from_client_address(client_address)
                    line = game.distributor.get_object_by_id(Distributor.OBJ_LINE, input_data['line'].id)
                    road = player.roads.pop()
                    player.pay_for_action(action)
                    line.add_road(road)
                    output_data = {'action': action, 'line': line, 'player': player, 'players': game.players, 'road': road}
                    self.broadcast_to_game(game.code, output_data)
                elif action == ActionFactory.BUILD_SETTLEMENT:
                    game_code = input_data['game_code']
                    game = self.games[game_code]
                    player = game.get_player_from_client_address(client_address)
                    node = game.distributor.get_object_by_id(Distributor.OBJ_NODE, input_data['node'].id)
                    settlement = player.settlements.pop()
                    player.pay_for_action(action)
                    node.add_settlement(settlement)
                    output_data = {'action': action, 'node': node, 'player': player, 'settlement': settlement} ### TODO: Player has spent a settlement
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
                    self.broadcast_to_game(game.code, {'action': action, 'player': player})
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
                elif action == ActionFactory.ROLL_DICE:
                    game_code = input_data['game_code']
                    game = self.games[game_code]
                    player = game.get_player_from_client_address(client_address)
                    dice_roll = game.roll_dice()
                    output_data = {'action': action, 'dice_roll': dice_roll, 'player': player, 'players': game.players}
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