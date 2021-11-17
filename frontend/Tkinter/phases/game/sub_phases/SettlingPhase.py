import textwrap
import tkinter
import tkinter.scrolledtext

from frontend.ColorUtils import ColorUtils
from frontend.GeneralUtils import GeneralUtils
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
    
    def setup_inner_frame_bottom_left(self):
        player_active = self.chaperone.player == self.chaperone.get_active_player()
        instruction_text = "It's your turn!" if player_active else 'Please wait for your turn'
        label_bg_color = '#90EE90' if player_active else '#F08080' ### LightGreen or LightCoral
        return super().setup_inner_frame_bottom_left(instruction_text, label_bg_color)
    
    def get_introductory_text(self):
        settling_order_text = '\n\n'.join([f'{player} will settle {GeneralUtils.get_ordinal(i)}' for i, player in enumerate(self.chaperone.players, 1)])
        return textwrap.dedent(f"""
            Hi {self.chaperone.player}, and welcome to Catan!

            A game of Catan begins with each player placing settlements on two nodes, with a single road leading away from each settlement.

            Players take it in turns to place settlements and roads, with turn-taking following the “snake draft” format, such that the player who settles first will be the player who settles last.

            Players are ordered randomly for the first round of settling.

            {settling_order_text}
        """)