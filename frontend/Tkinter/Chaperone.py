from catan.mechanics.Game import Game
from frontend.Tkinter.LobbyPhase import LobbyPhase
from frontend.Tkinter.MainPhase import MainPhase
from frontend.Tkinter.SettlePhase import SettlePhase
from frontend.Tkinter.HomePhase import HomePhase
from config import config

class Chaperone:
    def __init__(self):
        self.config = config
    
    def get_font(self):
        return (self.FONT_NAME, self.FONT_SIZE, self.FONT_WEIGHT)
    
    def set_num_hexagons(self, num_hexagons):
        self.num_hexagons = num_hexagons
    
    def start_home_phase(self):
        self.home_phase = HomePhase(self)
        self.home_phase.run()
    
    def start_lobby_phase(self):
        self.home_phase.root.destroy()
        self.lobby_phase = LobbyPhase(self)
        self.lobby_phase.run()
    
    def start_settle_phase(self):
        self.settle_phase = SettlePhase(self)
    
    def start_main_phase(self):
        self.lobby_phase.root.destroy()
        self.main_phase = MainPhase(self)
        game = Game(config, ['Will', 'Kate'], num_hexagons = self.num_hexagons)
        game.setup_board()
        game.setup_cards()
        game.setup_movable_pieces()
        self.main_phase.set_game(game)
        self.main_phase.run()