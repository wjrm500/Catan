from frontend.Tkinter.Chaperone import Chaperone
from catan.mechanics.Game import Game
from config import config
from frontend.Matplotlib import Matplotlib

# game = Game(config, ['Will', 'Kate'], 100)
# game.setup_board()
# game.setup_cards()
# game.setup_movable_pieces()
# Matplotlib.draw_board(game)
chaperone = Chaperone()
chaperone.start_setup_phase()