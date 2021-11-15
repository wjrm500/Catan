import tkinter
from tkinter import messagebox
from actions.ActionFactory import ActionFactory
from frontend.Tkinter.phases.primary.SettlingPhase import SettlingPhase
import json
import os

class Chaperone:
    def __init__(self, socket, queue):
        self.socket = socket
        self.queue = queue
        self.root = tkinter.Tk()
        self.root.after(100, self.check_queue)
        self.root.title('Catan')
        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)
        self.current_phase = None
        self.players = []
        self.player = ''
        self.main = False ### User is main client i.e. created game
        self.start_phase(SettlingPhase)
        exit()
    
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
    
    def display_error_text(self, error_text):
        self.current_phase.display_error_text(error_text)
    
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
        self.settle_phase = SettlingPhase(self)
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            os._exit(0)