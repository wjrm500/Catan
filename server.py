from actions.ActionFactory import ActionFactory
from backend.mechanics.Player import Player
from config import config
from backend.mechanics.Game import Game
import socket
import threading
import json
from pympler.asizeof import asizeof
import pickle

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
            
    def handle(self, client_conn):
        while True:
            try:
                client_address = client_conn.getpeername()
                from_client = client_conn.recv(1024).decode('utf-8')
                from_client = json.loads(from_client)
                print(f'Client: {client_address} || Data: {from_client}')
                action = from_client['action']
                if action == ActionFactory.ADD_PLAYER:
                    game_code = from_client['game_code']
                    game = self.games[game_code]
                    player = Player(from_client['player'], client_address)
                    game.add_player(player)
                    data = {'action': action, 'players': [player.name for player in game.players]}
                    self.broadcast(game_code, data)
                elif action == ActionFactory.CREATE_NEW_GAME:
                    num_hexagons = from_client['num_hexagons']
                    game = Game(config, num_hexagons)
                    game.main_client_address = client_address ### Use setter
                    game.clients = [client_address] ### Use add_client method and if first client set as creator (remove line above)
                    self.games[game.code] = game ###{'clients': [client_conn], 'delete': False, 'game': game, 'main_client': client_conn}
                    data = {'action': action, 'game_code': game.code}
                    self.broadcast(game_code, data)
                elif action == ActionFactory.JOIN_EXISTING_GAME:
                    game_code = from_client['game_code']
                    game = self.games[game_code]
                    game.clients.append(client_address) ### Use add_client method as above
                    data = {'action': action, 'game_code': game_code, 'players': [player.name for player in game.players]}
                    self.broadcast(game_code, data)
                elif action == ActionFactory.START_GAME:
                    game_code = from_client['game_code']
                    game = self.games[game_code]
                    game.setup_board()
                    game.setup_cards()
                    game.setup_movable_pieces()
                    game.started = True
                    self.broadcast(game_code, {'action': action, 'distributor': game.distributor})
            except:                    
                ### End any games for which the client was the main client
                game_codes_to_delete = []
                for game_code, game in self.games.items():
                    if game.main_client_address == client_address:
                        self.broadcast(game.code, {'action': ActionFactory.END_GAME})
                        game_codes_to_delete.append(game_code)

                ### If game started, end any games involving the client
                ### If game not yet started, simply remove client from game
                for game_code, game in self.games.items():
                    if client_address in game.clients:
                        if game.started:
                            self.broadcast(game.code, {'action': ActionFactory.END_GAME})
                            game_codes_to_delete.append(game_code)
                        else:
                            player = [player.name for player in game.players if player.address == client_address][0]
                            self.broadcast(game_code, {'action': ActionFactory.REMOVE_PLAYER, 'player': player})

                for game_code in game_codes_to_delete:
                    del self.games[game_code]

                

    
    def broadcast(self, game_code, message):
        for client_conn in self.games[game_code]['clients']:
            try:
                encoded_message = json.dumps(message).encode('utf-8')
            except:
                encoded_message = pickle.dumps(message)
            bytes_to_send = str(asizeof(encoded_message)).encode('utf-8')
            client_conn.send(bytes_to_send) ### Header
            client_conn.send(encoded_message)
    
    ### Handle client disconnect

server = Server()
server.serve()