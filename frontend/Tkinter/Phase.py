import tkinter

class Phase:
    BG_COLOR = '#ADD8E6'
    CURSOR_HAND = 'hand2'

    def __init__(self, chaperone):
        self.chaperone = chaperone
        self.root = tkinter.Tk()
        self.root.title('Catan')
        self.FONT_NAME = 'Arial' ### Could belong to a base class
        self.FONT_SIZE = '10'
        self.FONT_WEIGHT = 'bold'
    
    def get_font(self):
        return (self.FONT_NAME, self.FONT_SIZE, self.FONT_WEIGHT)