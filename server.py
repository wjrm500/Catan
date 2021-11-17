import json
import pickle
from pympler.asizeof import asizeof
import random
import socket
import threading

from actions.ActionFactory import ActionFactory
from backend.mechanics.Player import Player
from config import config
from backend.mechanics.Game import Game

class Server:
    LOCAL_HOST = '127.0.0.1'
    LOCAL_PORT = 9090

    def __init__(self):
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
                from_client = client.recv(1024).decode('utf-8')
                from_client = json.loads(from_client)
                print(f'Incoming... Client: {client_address} || Data: {from_client}')
                action = from_client['action']
                if action == ActionFactory.ADD_PLAYER:
                    game_code = from_client['game_code']
                    game = self.games[game_code]
                    player = Player(from_client['player'], client)
                    game.add_player(player)
                    data = {'action': action, 'players': [player.name for player in game.players]}
                    self.broadcast_to_game(game.code, data)
                elif action == ActionFactory.CREATE_NEW_GAME:
                    num_hexagons = from_client['num_hexagons']
                    game = Game(config, num_hexagons)
                    game.add_client(client)
                    self.games[game.code] = game
                    data = {'action': action, 'game_code': game.code}
                    self.broadcast_to_game(game.code, data)
                elif action == ActionFactory.JOIN_EXISTING_GAME:
                    game_code = from_client['game_code']
                    data = {'action': action}
                    if game_code in self.games:
                        game = self.games[game_code]
                        game.add_client(client)
                        data.update({'game_code': game.code, 'players': [player.name for player in game.players]})
                        self.broadcast_to_game(game.code, data)
                    else:
                        data['error'] = f'"{game_code}" is not a valid game code'
                        self.broadcast_to_client(client, data)
                elif action == ActionFactory.START_GAME:
                    game_code = from_client['game_code']
                    game = self.games[game_code]
                    game.setup_board()
                    game.setup_cards()
                    game.setup_movable_pieces()
                    game.randomise_player_order()
                    game.started = True
                    self.broadcast_to_game(game.code, {'action': action, 'distributor': game.distributor, 'players': [player.name for player in game.players]})
            except:                    
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
                        player = game.get_player(client_address)
                        game.delete_client_and_corresponding_player_if_applicable(client_address)
                        if game.started:
                            self.broadcast_to_game(game.code, {'action': ActionFactory.END_GAME})
                            game_codes_to_delete.append(game_code)
                        else:
                            self.broadcast_to_game(game_code, {'action': ActionFactory.REMOVE_PLAYER, 'player': player.name})

                for game_code in game_codes_to_delete:
                    del self.games[game_code]

                client.shutdown(2)
                client.close()
                break
        
    def broadcast_to_client(self, client, message):
        try:
            encoded_message = json.dumps(message).encode('utf-8')
        except:
            encoded_message = pickle.dumps(message)
        bytes_to_send = str(asizeof(encoded_message)).encode('utf-8')
        client.send(bytes_to_send) ### Header
        client.send(encoded_message)
        print(f'Outgoing... {message}')
    
    def broadcast_to_game(self, game_code, message):
        for client in self.games[game_code].clients.values():
            self.broadcast_to_client(client, message)
    
    ### Handle client disconnect

server = Server()
server.serve()