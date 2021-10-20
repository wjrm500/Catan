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
    
    def get_font(self):
        return (self.FONT_NAME, self.FONT_SIZE, self.FONT_WEIGHT)