import textwrap
import tkinter
import tkinter.scrolledtext

from frontend.ColorUtils import ColorUtils
from frontend.Tkinter.phases.game.GamePhase import GamePhase

class SettlingPhase(GamePhase):
    def __init__(self, chaperone):
        super().__init__(chaperone)
    
    def setup_inner_frame_middle_right(self): ### Specific to settling phase (the rest isn't)
        self.text_area = tkinter.scrolledtext.ScrolledText(self.inner_frame_middle_right, font = ('Arial', 12), padx = 10, wrap = 'word', background = ColorUtils.lighten_hex(self.BG_COLOR, 0.2))
        self.text_area.pack(padx = 10, pady = 10)
        self.text_area.config(state = 'normal')
        self.text_area.insert('end', self.get_introductory_text())
        self.text_area.yview('end')
        self.text_area.config(state = 'disabled')
    
    def get_introductory_text(self):
        return textwrap.dedent("""
            Welcome to Catan!

            A game of Catan begins with each player placing settlements on two nodes, with a single road leading away from each settlement.

            Players take it in turns to place settlements and roads, with turn-taking following the “snake draft” format, such that the player who settles first will be the player who settles last.

            Players are ordered randomly for the first round of settling.
        """)