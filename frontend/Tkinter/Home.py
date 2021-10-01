import tkinter
from .MainLoop import MainLoop
from catan.mechanics.Game import Game
from config import config

class Home:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry('500x500')
        self.root.title('Catan')
        self.num_hexagons_input = tkinter.Entry(self.root)
        self.num_hexagons_input.place(relx = 0.5, rely = 0.4, anchor = tkinter.CENTER)
        self.enter_button = tkinter.Button(self.root, text = 'Submit', foreground = 'white', background = 'red', width = 10, height = 2)
        self.enter_button.place(relx = 0.5, rely = 0.5, anchor = tkinter.CENTER)
        self.FONT_NAME = 'Arial' ### Could belong to a base class
        self.FONT_SIZE = '10'
        self.FONT_WEIGHT = 'bold'
    
    def get_font(self):
        return (self.FONT_NAME, self.FONT_SIZE, self.FONT_WEIGHT)

    def run(self):
        self.enter_button.bind('<Button-1>', self.go_to_main_loop)
        self.root.mainloop()
    
    def go_to_main_loop(self, event):
        num_hexagons = self.num_hexagons_input.get()
        error = None
        if num_hexagons.isnumeric():
            num_hexagons = int(num_hexagons)
            if num_hexagons in range(5, 50):
                self.root.destroy()
                game = Game(config, ['Will', 'Kate'], num_hexagons = num_hexagons)
                game.setup_board()
                game.setup_cards()
                game.setup_movable_pieces()
                tk = MainLoop(game)
                tk.run()
            else:
                error = 'Number of hexagons must be between 5 and 50'
        else:
            error = 'Input must be numeric'
        if error:
            error_text = tkinter.Text(self.root, font = self.get_font(), foreground = 'red', background = '#eeeeee', width = 25, height = 2, bd = 0)
            error_text.tag_configure('tag-center', justify = 'center')
            error_text.insert(tkinter.END, error, 'tag-center')
            error_text.place(relx = 0.5, rely = 0.6, anchor = tkinter.CENTER)

        