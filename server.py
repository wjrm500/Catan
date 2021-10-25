from config import config
from backend.mechanics.Game import Game
import socket
import threading
import random
import string
import re

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
            print(from_client)
            if re.search('^.+;.+$', from_client):
                action, data = from_client.split(';')
                if action == 'CREATE_NEW_GAME': ### TODO: Make constant
                    game = Game(config)
                    game_code = ''.join(random.choices(string.ascii_letters, k = 10))
                    self.games[game_code] = {
                        'clients': [client_conn],
                        'game': game,
                        'main_client': client_conn
                    }
                elif action == 'JOIN_EXISTING_GAME': ### TODO: Make constant
                    game_code = data
                    self.games[game_code]['clients'].append(client_conn)

server = Server()
server.serve()