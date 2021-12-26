import os
from PIL import Image, ImageTk
import tkinter
from tkinter import messagebox

from actions.ActionFactory import ActionFactory
from frontend.GeneralUtils import GeneralUtils as gutils
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
        self.settling_phase_text = ''
        self.winner_announced = False
    
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
            if gutils.safe_isinstance(self.current_phase, 'MainGamePhase'):
                self.display_winner()
        self.root.after(100, self.check_queue)
    
    def display_winner(self):
        if not self.winner_announced:
            game = self.player.game
            try:
                winner = next(player for player in self.players if player.victory_points() >= game.victory_point_limit)
                popup = tkinter.Toplevel(self.root, background = Phase.BG_COLOR)
                popup.geometry('250x250')
                popup.wm_title('Catan')
                popup.tkraise(self.root)
                frame = tkinter.Frame(popup, background = Phase.BG_COLOR)
                frame.place(anchor = tkinter.CENTER, relx = 0.5, rely = 0.5)

                canvas = tkinter.Canvas(frame, background = Phase.BG_COLOR, height = 75, width = 75, bd = 0, highlightthickness = 0)
                canvas.pack()
                image = Image.open(Phase.CELEBRATION_IMG_FILEPATH)
                resized_image = image.resize((75, 75), Image.ANTIALIAS)
                new_image = ImageTk.PhotoImage(resized_image)
                self.root.celebration_image = new_image ### Prevent garbage collection
                canvas.create_image(0, 0, image = new_image, anchor = tkinter.NW)

                tkinter.Label(frame, text = f'{winner.name} won!', background = Phase.BG_COLOR, font = ('Arial', 16, 'bold')).pack()
                button = tkinter.Button(frame, text = 'Acknowledge', command = popup.destroy, background = Phase.DARKER_BG_COLOR)
                button.pack(pady = 10)
                button.bind('<Motion>', lambda evt: self.root.configure(cursor = Phase.CURSOR_HAND))
                button.bind('<Leave>', lambda evt: self.root.configure(cursor = Phase.CURSOR_DEFAULT))

                tkinter.Label(frame, text = 'Scores', background = Phase.BG_COLOR, font = ('Courier New', 12, 'bold')).pack()

                max_player_name_len = max(len(player.name) for player in game.players)
                for player in sorted(game.players, key = lambda player: player.victory_points(), reverse = True):
                    tkinter.Label(frame, text = f'{player.name.ljust(max_player_name_len)}   {player.victory_points()}', background = Phase.BG_COLOR, font = ('Courier New', 10)).pack()
                
                if self.main: ### TODO: Delete next couple of lines in production version?
                    headings = ['datetime', 'winner', 'player_scores', 'rounds_completed', 'longest_road_holder', 'longest_road', 'largest_army_holder', 'largest_army']
                    filename = 'scores.txt'
                    file_existed = os.path.exists(filename)
                    with open(filename, 'a') as file:
                        if not file_existed:
                            file.write(f'{";".join(headings)}\n')
                        datetime_now = datetime.now().strftime('%Y-%M-%d %H:%M:%S')
                        player_scores = ','.join([f'{player.name} {player.victory_points()}' for player in game.players])
                        values = [
                            datetime_now,
                            winner.name,
                            player_scores,
                            game.rounds_completed,
                            game.longest_road['player'],
                            game.longest_road['road_length'],
                            game.largest_army['player'],
                            game.largest_army['army_size']
                        ]
                        values = list(map(str, values))
                        file.write(f'{";".join(values)}\n')

                self.winner_announced = True
            except StopIteration:
                pass
    
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
    
    def build_village(self, node):
        data = {
            'action': ActionFactory.BUILD_VILLAGE,
            'game_code': self.game_code,
            'node_id': node.id
        }
        self.client.interface.send_data(self.client.socket, data)

    def build_road(self, line, from_development_card = False, road_building_turn_index = None):
        data = {
            'action': ActionFactory.BUILD_ROAD,
            'from_development_card': from_development_card,
            'game_code': self.game_code,
            'line_id': line.id,
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
            'hexagon_id': hexagon.id
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
            'node_id': node.id
        }
        self.client.interface.send_data(self.client.socket, data)
    
    def move_robber_to_desert(self):
        data = {
            'action': ActionFactory.MOVE_ROBBER_TO_DESERT,
            'game_code': self.game_code
        }
        self.client.interface.send_data(self.client.socket, data)
    
    def swap_cards(self, swap_card_resource_types):
        data = {
            'action': ActionFactory.SWAP_CARDS,
            'game_code': self.game_code,
            'swap_card_resource_types': swap_card_resource_types
        }
        self.client.interface.send_data(self.client.socket, data)
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            os._exit(0)