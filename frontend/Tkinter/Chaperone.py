import tkinter
from actions.ActionFactory import ActionFactory
from frontend.Tkinter.phases.primary.setup.ExistingGamePhase import ExistingGamePhase
from frontend.Tkinter.phases.primary.setup.HomePhase import HomePhase
from frontend.Tkinter.phases.primary.setup.NewGamePhase import NewGamePhase
from frontend.Tkinter.phases.primary.setup.LobbyPhase import LobbyPhase
from frontend.Tkinter.phases.primary.GamePhase import GamePhase
from frontend.Tkinter.phases.primary.SettlePhase import SettlePhase
import json

class Chaperone:
    def __init__(self, socket, queue):
        self.socket = socket
        self.queue = queue
        self.root = tkinter.Tk()
        self.root.after(100, self.check_queue)
        self.root.title('Catan')
        self.current_phase = None
        self.players = []
    
    def get_font(self):
        return (self.FONT_NAME, self.FONT_SIZE, self.FONT_WEIGHT)
    
    def check_queue(self):
        ### Might be better to avoid polling and use event_generate - https://stackoverflow.com/questions/7141509/tkinter-wait-for-item-in-queue
        while self.queue.empty() is False:
            print(0)
            data = self.queue.get(timeout = 0.1)
            print(1)
            action_str, param = data.decode('utf-8').split(';')
            print(2)
            action = ActionFactory.get_action(action_str)
            print(3)
            action.callback(self, param)
            print(4)
            self.update_gui()
            print(5)
        self.root.after(100, self.check_queue)
    
    def update_gui(self):
        self.current_phase.update_gui()
    
    def start_phase(self, phase):
        if self.current_phase is not None:
            self.current_phase.outer_frame.destroy()
        self.current_phase = phase(self)
        self.current_phase.run()
    
    def add_player(self, name):
        to_send = json.dumps({
            'action': ActionFactory.ADD_PLAYER,
            'game_code': self.game_code,
            'player': name
        })
        self.socket.send(to_send.encode('utf-8'))
    
    def create_new_game(self, num_hexagons):
        to_send = json.dumps({
            'action': ActionFactory.CREATE_NEW_GAME,
            'num_hexagons': num_hexagons
        })
        self.socket.send(to_send.encode('utf-8'))
    
    def get_players(self):
        to_send = json.dumps({
            'action': ActionFactory.GET_PLAYERS,
            'game_code': self.game_code
        })
        self.socket.send(to_send.encode('utf-8'))
    
    def join_existing_game(self, game_code):
        to_send = json.dumps({
            'action': ActionFactory.JOIN_EXISTING_GAME,
            'game_code': game_code
        })
        self.socket.send(to_send.encode('utf-8'))
    
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