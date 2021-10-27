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
        self.player = ''
        self.main = False ### User is main client i.e. created game
    
    def get_font(self):
        return (self.FONT_NAME, self.FONT_SIZE, self.FONT_WEIGHT)
    
    def check_queue(self):
        ### Might be better to avoid polling and use event_generate - https://stackoverflow.com/questions/7141509/tkinter-wait-for-item-in-queue
        while self.queue.empty() is False:
            data = self.queue.get(timeout = 0.1)
            action = ActionFactory.get_action(data['action'])
            action.callback(self, data)
            self.update_gui()
        self.root.after(100, self.check_queue)
    
    def update_gui(self):
        self.current_phase.update_gui()
    
    def start_phase(self, phase, destroy_root = False):
        if self.current_phase is not None:
            to_destroy = self.current_phase.root if destroy_root else self.current_phase.outer_frame
            to_destroy.destroy()
        self.current_phase = phase(self)
        self.current_phase.run()
    
    def add_player(self, name):
        self.player = name
        to_send = json.dumps({
            'action': ActionFactory.ADD_PLAYER,
            'game_code': self.game_code,
            'player': name
        })
        self.socket.send(to_send.encode('utf-8'))
    
    def create_new_game(self, num_hexagons):
        self.main = True
        to_send = json.dumps({
            'action': ActionFactory.CREATE_NEW_GAME,
            'num_hexagons': num_hexagons
        })
        self.socket.send(to_send.encode('utf-8'))
    
    def join_existing_game(self, game_code):
        to_send = json.dumps({
            'action': ActionFactory.JOIN_EXISTING_GAME,
            'game_code': game_code
        })
        self.socket.send(to_send.encode('utf-8'))
    
    def start_game(self):
        to_send = json.dumps({
            'action': ActionFactory.START_GAME,
            'game_code': self.game_code
        })
        self.socket.send(to_send.encode('utf-8'))
    
    def start_settle_phase(self):
        self.settle_phase = SettlePhase(self)