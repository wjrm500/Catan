import tkinter

class Phase:
    BG_COLOR = '#ADD8E6'
    CURSOR_HAND = 'hand2'
    FONT_NAME = 'Arial'
    FONT_SIZE = '10'
    FONT_WEIGHT = 'bold'

    def __init__(self, chaperone):
        self.chaperone = chaperone
        self.root = chaperone.root
    
    def get_font(self, font_name = None, font_size = None, font_weight = None):
        return (
            font_name or self.FONT_NAME,
            font_size or self.FONT_SIZE,
            font_weight or self.FONT_WEIGHT
        )
    
    def update_gui(self):
        pass