from catan.mechanics.Game import Game
from config import config
from frontend.Matplotlib import Matplotlib

game = Game(config)
game.setup_board()
Matplotlib.draw_board(game)