import tkinter
from frontend.Tkinter.phases.game.GamePhase import GamePhase

class MainGamePhase(GamePhase):
    def update_active_player_index(self):
        self.active_player_index += 1
        if self.active_player_index > len(self.players) - 1:
            self.active_player_index = 0
    
    def setup_inner_frame_top_right(self):
        super().setup_inner_frame_top_right('MAIN GAME PHASE')
    
    def setup_inner_frame_middle_right(self):
        self.text_area = tkinter.scrolledtext.ScrolledText(self.inner_frame_middle_right)
        self.text_area.pack(padx = 10, pady = 10)
    
    def setup_inner_frame_bottom_left(self):
        client_active = self.client_active()
        instruction_text = "It's your turn!" if client_active else 'Please wait for your turn'
        label_bg_color = '#90EE90' if client_active else '#F08080' ### LightGreen or LightCoral
        return super().setup_inner_frame_bottom_left(instruction_text, label_bg_color)