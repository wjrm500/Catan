from catan.mechanics.Game import Game
from config import config
from frontend.Matplotlib import Matplotlib
from frontend.Tkinter import TkinterFrontend as Tkinter

game = Game(config, ['Will', 'Kate'], 35)
game.setup_board()
game.setup_cards()
game.setup_movable_pieces()
# game.start()
# Matplotlib.draw_board(game)
Tkinter.draw_board(game)