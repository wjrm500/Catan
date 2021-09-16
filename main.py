from catan.mechanics.Game import Game
from config import config
from frontend.Matplotlib import Matplotlib
from frontend.Tkinter import TkinterFrontend

game = Game(config, ['Will', 'Kate'], 50)
game.setup_board()
game.setup_cards()
game.setup_movable_pieces()
# game.start()
# Matplotlib.draw_board(game)
tk = TkinterFrontend(game)
tk.run()