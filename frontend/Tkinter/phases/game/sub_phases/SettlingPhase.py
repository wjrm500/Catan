import tkinter
import tkinter.scrolledtext

from frontend.ColorUtils import ColorUtils
from frontend.GeneralUtils import GeneralUtils
from frontend.Tkinter.phases.game.GamePhase import GamePhase
from frontend.Tkinter.rendering.HexagonRendering import HexagonRendering

class SettlingPhase(GamePhase):
    def __init__(self, chaperone):
        super().__init__(chaperone)
        self.active_player_index_incrementing = True
    
    def update_active_player_index(self):
        at_start = self.active_player_index == 0
        at_end = self.active_player_index == len(self.chaperone.players) - 1
        turning_at_start = at_start and not self.active_player_index_incrementing
        turning_at_end = at_end and self.active_player_index_incrementing
        if not turning_at_start and not turning_at_end:
            self.active_player_index += 1 if self.active_player_index_incrementing else -1
        if at_start:
            self.active_player_index_incrementing = True
        if at_end:
            self.active_player_index_incrementing = False
        
    def setup_inner_frame_top_right(self):
        super().setup_inner_frame_top_right('SETTLING PHASE')
    
    def setup_inner_frame_middle_left(self):
        canvas_mode = HexagonRendering.CANVAS_MODE_BUILD_SETTLEMENT if self.client_active() else HexagonRendering.CANVAS_MODE_DISABLED
        return super().setup_inner_frame_middle_left(canvas_mode)
    
    def setup_inner_frame_middle_right(self):
        self.text_area = tkinter.scrolledtext.ScrolledText(self.inner_frame_middle_right, font = ('Arial', 12), padx = 10, pady = 10, wrap = 'word', background = ColorUtils.lighten_hex(self.BG_COLOR, 0.2))
        self.text_area.config(state = 'normal')
        self.text_area.insert('end', self.get_introductory_text())
        self.text_area.yview('end')
        self.text_area.config(state = 'disabled')
    
    def setup_inner_frame_bottom_left(self):
        client_active = self.client_active()
        instruction_text = 'Build a settlement!' if client_active else 'Please wait for your turn'
        label_bg_color = '#90EE90' if client_active else '#F08080' ### LightGreen or LightCoral
        return super().setup_inner_frame_bottom_left(instruction_text, label_bg_color)
    
    def get_introductory_text(self):
        settling_order_text = '\n\n'.join([f'{player.name} will settle {GeneralUtils.get_ordinal(i)}' for i, player in enumerate(self.chaperone.players, 1)])
        return f"""Hi {self.chaperone.player.name}, and welcome to Catan!

A game of Catan begins with each player placing settlements on two nodes, with a single road leading away from each settlement.

Players take it in turns to place settlements and roads, with turn-taking following the “snake draft” format, such that the player who settles first will be the player who settles last.

Players are ordered randomly for the first round of settling.

{settling_order_text}

Round 1 commencing...

It is {self.active_player().name}'s turn to settle..."""

    def activate_button(self):
        self.button_text.set('Proceed')
        self.button['state'] = 'normal'
        self.button.configure({'background': '#90EE90'}) ### LightGreen
        self.button.bind('<Motion>', lambda evt: self.root.configure(cursor = self.CURSOR_HAND))
        self.button.bind('<Leave>', lambda evt: self.root.configure(cursor = self.CURSOR_DEFAULT))
        self.button.bind('<Button-1>', self.start_game_proper)
    
    def start_game_proper(self, event):
        self.root.configure(cursor = self.CURSOR_DEFAULT)
        self.chaperone.start_game_proper()
    
    def run(self):
        self.root.bind('<Configure>', self.resize_text_area, '+')
        super().run()
    
    def resize_text_area(self, event):
        self.root.update_idletasks()
        ifmr = self.inner_frame_middle_right
        self.text_area.place(in_ = ifmr, x = 10, y = 10, height = ifmr.winfo_height() - 20, width = ifmr.winfo_width() - 20)