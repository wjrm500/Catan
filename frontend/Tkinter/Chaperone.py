import os
import tkinter
from tkinter import messagebox

from actions.ActionFactory import ActionFactory
from frontend.Tkinter.Style import Style
from frontend.Tkinter.phases.Phase import Phase

class Chaperone:
    def __init__(self, client, queue):
        self.client = client
        self.queue = queue
        self.root = tkinter.Tk()
        self.root.after(100, self.check_queue)
        self.root.title('Catan')
        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)
        self.root.state('zoomed')
        Style().setup()
        self.current_phase = None
        self.players = []
        self.player = None
        self.main = False ### User is main client i.e. created game
        self.game_code = ''
    
    def get_player_from_id(self, id):
        return next(player for player in self.players if player.id == id)

    def update_players(self, players):
        self.players = players
        if self.player is not None:
            for player in self.players:
                if player.id == self.player.id:
                    self.player = player
    
    def get_font(self):
        return (self.FONT_NAME, self.FONT_SIZE, self.FONT_WEIGHT)
    
    def check_queue(self):
        ### Might be better to avoid polling and use event_generate - https://stackoverflow.com/questions/7141509/tkinter-wait-for-item-in-queue
        while self.queue.empty() is False:
            data = self.queue.get(timeout = 0.1)
            action = ActionFactory.get_action(data['action'])
            action.callback(self, data)
        self.root.after(100, self.check_queue)
    
    def display_error_text(self, error_text):
        self.current_phase.display_error_text(error_text)
    
    def start_phase(self, phase, to_destroy = None):
        if self.current_phase is not None:
            to_destroy = to_destroy or self.current_phase.outer_frame
            to_destroy.destroy()
        self.current_phase = phase(self)
        self.root.configure(cursor = Phase.CURSOR_DEFAULT)
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

    def build_road(self, line, from_development_card = False, road_building_turn_index = None):
        data = {
            'action': ActionFactory.BUILD_ROAD,
            'from_development_card': from_development_card,
            'game_code': self.game_code,
            'line': line,
            'road_building_turn_index': road_building_turn_index
        }
        self.client.interface.send_data(self.client.socket, data)

    def start_game_proper(self):
        data = {
            'action': ActionFactory.START_GAME_PROPER,
            'game_code': self.game_code
        }
        self.client.interface.send_data(self.client.socket, data)
    
    def roll_dice(self):
        data = {
            'action': ActionFactory.ROLL_DICE,
            'game_code': self.game_code
        }
        self.client.interface.send_data(self.client.socket, data)
    
    def end_turn(self):
        data = {
            'action': ActionFactory.END_TURN,
            'game_code': self.game_code
        }
        self.client.interface.send_data(self.client.socket, data)
    
    def place_robber(self, hexagon, from_development_card):
        data = {
            'action': ActionFactory.PLACE_ROBBER,
            'from_development_card': from_development_card,
            'game_code': self.game_code,
            'hexagon': hexagon
        }
        self.client.interface.send_data(self.client.socket, data)
    
    def trade_with_bank(self, give_type, receive_type):
        data = {
            'action': ActionFactory.TRADE_WITH_BANK,
            'game_code': self.game_code,
            'give_type': give_type,
            'receive_type': receive_type
        }
        self.client.interface.send_data(self.client.socket, data)

    def buy_development_card(self):
        data = {
            'action': ActionFactory.BUY_DEVELOPMENT_CARD,
            'game_code': self.game_code
        }
        self.client.interface.send_data(self.client.socket, data)
    
    def play_monopoly_card(self, resource_type):
        data = {
            'action': ActionFactory.PLAY_MONOPOLY_CARD,
            'game_code': self.game_code,
            'resource_type': resource_type
        }
        self.client.interface.send_data(self.client.socket, data)
    
    def play_year_of_plenty_card(self, resource_type, year_of_plenty_turn_index):
        data = {
            'action': ActionFactory.PLAY_YEAR_OF_PLENTY_CARD,
            'game_code': self.game_code,
            'resource_type': resource_type,
            'year_of_plenty_turn_index': year_of_plenty_turn_index
        }
        self.client.interface.send_data(self.client.socket, data)
    
    def upgrade_settlement(self, node):
        data = {
            'action': ActionFactory.UPGRADE_SETTLEMENT,
            'game_code': self.game_code,
            'node': node
        }
        self.client.interface.send_data(self.client.socket, data)
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            os._exit(0)