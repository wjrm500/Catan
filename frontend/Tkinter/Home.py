import tkinter
from .MainLoop import MainLoop
from catan.mechanics.Game import Game
from config import config

class Home:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry('500x500')
        self.root.title('Catan')
        self.root.minsize(250, 250)
        self.FONT_NAME = 'Arial' ### Could belong to a base class
        self.FONT_SIZE = '10'
        self.FONT_WEIGHT = 'bold'
        label = 'Number of hexagons:'
        self.num_hexagons_label = tkinter.Text(self.root, font = self.get_font(), foreground = 'black', background = '#eeeeee', width = 25, height = 2, bd = 0)
        self.num_hexagons_label.tag_configure('tag-center', justify = 'center')
        self.num_hexagons_label.insert(tkinter.END, label, 'tag-center')
        self.num_hexagons_label.place(relx = 0.5, rely = 0.32, anchor = tkinter.CENTER)
        self.num_hexagons_input = tkinter.Entry(self.root)
        self.num_hexagons_input.place(relx = 0.5, rely = 0.4, anchor = tkinter.CENTER)
        self.num_hexagons_input.focus()
        self.enter_button = tkinter.Button(self.root, text = 'SUBMIT', font = self.get_font(), foreground = 'white', background = 'red', width = 10, height = 1)
        self.enter_button.place(relx = 0.5, rely = 0.55, anchor = tkinter.CENTER)    
    
    def get_font(self):
        return (self.FONT_NAME, self.FONT_SIZE, self.FONT_WEIGHT)

    def run(self):
        self.enter_button.bind('<Button-1>', self.go_to_main_loop)
        self.num_hexagons_input.bind('<Return>', self.go_to_main_loop)
        self.root.mainloop()
    
    def go_to_main_loop(self, event):
        num_hexagons = self.num_hexagons_input.get()
        error = None
        if num_hexagons.isnumeric():
            num_hexagons = int(num_hexagons)
            if num_hexagons in range(5, 51):
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

        