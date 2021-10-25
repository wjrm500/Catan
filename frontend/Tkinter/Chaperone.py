import tkinter
from frontend.Tkinter.phases.primary.setup.ExistingGamePhase import ExistingGamePhase
from frontend.Tkinter.phases.primary.setup.HomePhase import HomePhase
from frontend.Tkinter.phases.primary.setup.NewGamePhase import NewGamePhase
from frontend.Tkinter.phases.primary.setup.LobbyPhase import LobbyPhase
from frontend.Tkinter.phases.primary.GamePhase import GamePhase
from frontend.Tkinter.phases.primary.SettlePhase import SettlePhase
import json

class Chaperone:
    def __init__(self, socket):
        self.socket = socket
        self.root = tkinter.Tk()
        self.root.title('Catan')
    
    def get_font(self):
        return (self.FONT_NAME, self.FONT_SIZE, self.FONT_WEIGHT)
    
    def start_home_phase(self):
        self.home_phase = HomePhase(self)
        self.home_phase.run()
    
    def start_new_game_phase(self):
        self.home_phase.outer_frame.destroy()
        self.new_game_phase = NewGamePhase(self)
        self.new_game_phase.run()
    
    def create_new_game(self, num_hexagons):
        self.socket.send(f'CREATE_NEW_GAME;{num_hexagons}'.encode('utf-8'))
        from_server = self.socket.recv(1024) ### Game code
        from_server = from_server.decode('utf-8')
        self.game_code = from_server
    
    def start_existing_game_phase(self):
        self.home_phase.outer_frame.destroy()
        self.existing_game_phase = ExistingGamePhase(self)
        self.existing_game_phase.run()
    
    def join_existing_game(self, game_code):
        self.game_code = game_code
        self.socket.send(f'JOIN_EXISTING_GAME;{game_code}'.encode('utf-8'))
    
    def start_lobby_phase(self, previous_phase): ### Previous phase could be new game phase or existing game phase
        previous_phase.outer_frame.destroy()
        self.lobby_phase = LobbyPhase(self)
        self.lobby_phase.run()
    
    def add_player(self, name):
        self.socket.send(f'ADD_PLAYER;{name}'.encode('utf-8'))
    
    def get_players(self):
        self.socket.send(f'GET_PLAYERS;{self.game_code}'.encode('utf-8'))
        from_server = self.socket.recv(1024) ### Player names
        return json.loads(from_server)
    
    def start_settle_phase(self):
        self.settle_phase = SettlePhase(self)
    
    def start_main_phase(self):
        self.lobby_phase.root.destroy()
        self.main_phase = GamePhase(self)
        self.game.setup_board()
        self.game.setup_cards()
        self.game.setup_movable_pieces()
        self.main_phase.set_game(self.game)
        self.main_phase.run()