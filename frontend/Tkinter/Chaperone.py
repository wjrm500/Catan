import os
import tkinter
from tkinter import messagebox

from actions.ActionFactory import ActionFactory

class Chaperone:
    def __init__(self, client, queue):
        self.client = client
        self.queue = queue
        self.root = tkinter.Tk()
        self.root.after(100, self.check_queue)
        self.root.title('Catan')
        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)
        self.current_phase = None
        self.players = []
        self.player = None
        self.main = False ### User is main client i.e. created game
        self.active_player_index = 0
        self.game_code = ''
    
    def update_active_player_index(self):
        self.active_player_index += 1
        if self.active_player_index > len(self.players) - 1:
            self.active_player_index = 1
    
    def get_player_from_id(self, id):
        return next(player for player in self.players if player.id == id)

    def update_players(self, players):
        self.players = players
        if self.player is not None:
            for player in self.players:
                if player.id == self.player.id:
                    self.player = player
    
    def get_active_player(self):
        return self.players[self.active_player_index]
    
    def active(self):
        return self.player.id == self.get_active_player().id
    
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
        if hasattr(self.current_phase, 'update_gui') and callable(getattr(self.current_phase, 'update_gui')):
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
        data = {
            'action': ActionFactory.ADD_PLAYER,
            'game_code': self.game_code,
            'player': name
        }
        self.client.interface.send_data(self.client.socket, data) ### Tried using a decorator for this (as appears in other methods but couldn't get it to work)
    
    def create_new_game(self, num_hexagons):
        data = {
            'action': ActionFactory.CREATE_NEW_GAME,
            'num_hexagons': num_hexagons
        }
        self.client.interface.send_data(self.client.socket, data)

    def join_existing_game(self, game_code):
        data = {
            'action': ActionFactory.JOIN_EXISTING_GAME,
            'game_code': game_code
        }
        self.client.interface.send_data(self.client.socket, data)
    
    def start_game(self):
        data = {
            'action': ActionFactory.START_GAME,
            'game_code': self.game_code
        }
        self.client.interface.send_data(self.client.socket, data)
    
    def build_settlement(self, node):
        data = {
            'action': ActionFactory.BUILD_SETTLEMENT,
            'game_code': self.game_code,
            'node': node
        }
        self.client.interface.send_data(self.client.socket, data)

    def build_road(self, line):
        data = {
            'action': ActionFactory.BUILD_ROAD,
            'game_code': self.game_code,
            'line': line
        }
        self.client.interface.send_data(self.client.socket, data)
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            os._exit(0)