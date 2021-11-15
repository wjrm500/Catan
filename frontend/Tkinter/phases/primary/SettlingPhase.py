import tkinter
from frontend.Tkinter.phases.Phase import Phase
from frontend.Tkinter.rendering.HexagonRendering import HexagonRendering

class SettlingPhase(Phase):
    def __init__(self, chaperone):
        super().__init__(chaperone)
        self.root.geometry('1000x500')
        self.frames = []
        self.inner_frame = tkinter.Frame(self.root, background = '#dddddd')
        self.inner_frame.pack(fill = 'both', expand = True, padx = 10, pady = 10)
        inner_frame_top = tkinter.Frame(self.inner_frame, background = '#cccccc', height = 50)
        inner_frame_top.pack(side = tkinter.TOP, fill = 'x')
        inner_frame_top_left = tkinter.Frame(inner_frame_top, background = '#bbbbbb', height = 50)
        inner_frame_top_right = tkinter.Frame(inner_frame_top, background = '#aaaaaa', height = 50)
        inner_frame_top_left.place(in_ = inner_frame_top, anchor = 'w', relheight = 1.0, relwidth = 0.5, relx = 0.5, rely = 0.5)
        inner_frame_top_right.place(in_ = inner_frame_top, anchor = 'e', relheight = 1.0, relwidth = 0.5, relx = 0.5, rely = 0.5)
        inner_frame_bottom = tkinter.Frame(self.inner_frame, background = '#999999')
        inner_frame_bottom.pack(side = tkinter.TOP, fill = 'both', expand = True)
        inner_frame_bottom_left = tkinter.Frame(inner_frame_bottom, background = 'red')
        self.inner_frame_bottom_right = tkinter.Frame(inner_frame_bottom, background = '#777777')
        inner_frame_bottom_left.place(in_ = inner_frame_bottom, anchor = 'e', relheight = 1.0, relwidth = 0.5, relx = 0.5, rely = 0.5)
        self.inner_frame_bottom_right.place(in_ = inner_frame_bottom, anchor = 'w', relheight = 1.0, relwidth = 0.5, relx = 0.5, rely = 0.5)
        self.canvas = tkinter.Canvas(inner_frame_bottom_left, background = 'lightblue', bd = 0, highlightthickness = 0)
        self.canvas.pack(expand = True)
        self.hexagon_rendering = HexagonRendering(self)
    
    def run(self):
        self.root.bind('<Configure>', self.hexagon_rendering.handle_resize)
        self.canvas.bind('<Motion>', lambda evt: self.hexagon_rendering.handle_motion(evt))
        self.canvas.bind('<Leave>', self.hexagon_rendering.unfocus_focused_hexagons)
        self.root.mainloop()