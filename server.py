from actions.ActionFactory import ActionFactory
from config import config
from backend.mechanics.Game import Game
import socket
import threading
import random
import string
import json

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
            from_client = client_conn.recv(1024).decode('utf-8')
            from_client = json.loads(from_client)
            print(f'Client: {client_conn.getpeername()} || Data: {from_client}')
            action = from_client['action']
            if action == ActionFactory.ADD_PLAYER:
                game_code = from_client['game_code']
                player = from_client['player']
                self.games[game_code]['game'].players.append(player)
                players = self.games[game_code]['game'].players
                data = {'action': action, 'players': players}
                self.broadcast(game_code, data)
            elif action == ActionFactory.CREATE_NEW_GAME:
                num_hexagons = from_client['num_hexagons']
                game = Game(config, num_hexagons)
                game_code = ''.join(random.choices(string.ascii_lowercase, k = 5))
                self.games[game_code] = {'clients': [client_conn], 'game': game, 'main_client': client_conn}
                data = {'action': action, 'game_code': game_code}
                self.broadcast(game_code, data)
            elif action == ActionFactory.JOIN_EXISTING_GAME:
                game_code = from_client['game_code']
                self.games[game_code]['clients'].append(client_conn)
                players = self.games[game_code]['game'].players
                data = {'action': action, 'game_code': game_code, 'players': players}
                self.broadcast(game_code, data)
    
    def broadcast(self, game_code, message):
        for client_conn in self.games[game_code]['clients']:
            client_conn.send(json.dumps(message).encode('utf-8'))
    
    ### Handle client disconnect

server = Server()
server.serve()