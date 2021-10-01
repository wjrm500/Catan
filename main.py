from catan.mechanics.Game import Game
from config import config
from frontend.Matplotlib import Matplotlib
from frontend.Tkinter.Home import Home

game = Game(config, ['Will', 'Kate'], 100)
game.setup_board()
game.setup_cards()
game.setup_movable_pieces()
# Matplotlib.draw_board(game)
tk = Home()
tk.run()