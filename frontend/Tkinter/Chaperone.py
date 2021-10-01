from catan.mechanics.Game import Game
from frontend.Tkinter.MainPhase import MainPhase
from frontend.Tkinter.SettlePhase import SettlePhase
from frontend.Tkinter.SetupPhase import SetupPhase
from config import config

class Chaperone:
    def __init__(self):
        self.config = config
    
    def get_font(self):
        return (self.FONT_NAME, self.FONT_SIZE, self.FONT_WEIGHT)
    
    def start_setup_phase(self):
        self.setup_phase = SetupPhase(self)
        self.setup_phase.run()
    
    def start_settle_phase(self):
        self.settle_phase = SettlePhase(self)
    
    def start_main_phase(self, num_hexagons):
        self.setup_phase.root.destroy()
        self.main_phase = MainPhase(self)
        game = Game(config, ['Will', 'Kate'], num_hexagons = num_hexagons)
        game.setup_board()
        game.setup_cards()
        game.setup_movable_pieces()
        self.main_phase.set_game(game)
        self.main_phase.run()