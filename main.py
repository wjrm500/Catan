from catan.mechanics.Game import Game
from config import config
from frontend.Matplotlib import Matplotlib

game = Game(config, ['Will', 'Kate'])
game.setup_board()
game.setup_cards()
game.setup_movable_pieces()
# game.start()
Matplotlib.draw_board(game)