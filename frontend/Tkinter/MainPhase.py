from frontend.Tkinter.rendering.HexagonRendering import HexagonRendering
import tkinter
from .Phase import Phase

class MainPhase(Phase):
    def __init__(self, chaperone):
        super().__init__(chaperone)
        self.root.geometry('1000x500')
        self.left_frame = tkinter.Frame(self.root)
        self.right_frame = tkinter.Frame(self.root, background = 'white')
        self.left_frame.grid(row = 0, column = 0, sticky = 'nsew')
        self.right_frame.grid(row = 0, column = 1, sticky = 'nsew')
        self.root.grid_columnconfigure(0, weight = 1, uniform = 'group1')
        self.root.grid_columnconfigure(1, weight = 1, uniform = 'group1')
        self.root.grid_rowconfigure(0, weight = 1)
        self.canvas = tkinter.Canvas(self.left_frame, background = 'lightblue')
        self.canvas.pack(expand = True)
        self.hexagon_rendering = HexagonRendering(self)
    
    def set_game(self, game):
        self.game = game
        self.hexagon_rendering.game = game
    
    def run(self):
        self.root.bind('<Configure>', self.hexagon_rendering.handle_resize)
        self.canvas.bind('<Motion>', lambda evt: self.hexagon_rendering.focus_hexagons(evt))
        self.right_frame.bind('<Motion>', self.hexagon_rendering.reset_focused_hexagons)
        self.root.mainloop()