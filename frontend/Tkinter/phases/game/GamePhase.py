import abc
from functools import partial
import tkinter
import tkinter.scrolledtext

from frontend.Tkinter.phases.Phase import Phase
from frontend.Tkinter.rendering.HexagonRendering import HexagonRendering

class GamePhase(Phase, abc.ABC):
    def __init__(self, chaperone):
        super().__init__(chaperone)
        self.root.geometry('1000x500')
        self.frames = {}
        self.setup_frames()
        self.setup_inner_frame_top_right()
        self.setup_inner_frame_middle_left()
        self.setup_inner_frame_middle_right()
        self.setup_inner_frame_bottom_left()
        self.setup_inner_frame_bottom_right()
    
    def setup_frames(self):
        standard_frame = partial(tkinter.Frame, background = self.BG_COLOR, highlightbackground = self.BG_COLOR)
        place_frame = lambda what, where, anchor: what.place(in_ = where, anchor = anchor, relheight = 1.0, relwidth = 0.5, relx = 0.5, rely = 0.5)

        """
        Level 1 frames
        """
        self.inner_frame = standard_frame(self.root)
        self.inner_frame.pack(fill = 'both', expand = True, padx = 10, pady = 10)

        """
        Level 2 frames
        """
        # Top
        self.inner_frame_top = standard_frame(self.inner_frame, height = 50)
        self.inner_frame_top.pack(side = tkinter.TOP, fill = 'x')

        # Middle
        self.inner_frame_middle = standard_frame(self.inner_frame)
        self.inner_frame_middle.pack(side = tkinter.TOP, fill = 'both', expand = True)

        # Bottom
        self.inner_frame_bottom = standard_frame(self.inner_frame, height = 50)
        self.inner_frame_bottom.pack(side = tkinter.BOTTOM, fill = 'x')

        """
        Level 3 frames
        """
        # Top
        self.inner_frame_top_left = standard_frame(self.inner_frame_top, height = 50)
        place_frame(self.inner_frame_top_left, where = self.inner_frame_top, anchor = tkinter.E)
        self.inner_frame_top_right = standard_frame(self.inner_frame_top, height = 50)
        place_frame(self.inner_frame_top_right, where = self.inner_frame_top, anchor = tkinter.W)
        
        #  Middle
        self.inner_frame_middle_left = standard_frame(self.inner_frame_middle)
        place_frame(self.inner_frame_middle_left, where = self.inner_frame_middle, anchor = tkinter.E)
        self.inner_frame_middle_right = standard_frame(self.inner_frame_middle)
        place_frame(self.inner_frame_middle_right, where = self.inner_frame_middle, anchor = tkinter.W)
        
        # Bottom
        self.inner_frame_bottom_left = standard_frame(self.inner_frame_bottom, height = 50)
        place_frame(self.inner_frame_bottom_left, where = self.inner_frame_bottom, anchor = tkinter.E)
        self.inner_frame_bottom_right = standard_frame(self.inner_frame_bottom, height = 50, padx = 10)
        place_frame(self.inner_frame_bottom_right, where = self.inner_frame_bottom, anchor = tkinter.W)
    
    def setup_inner_frame_top_right(self):
        block_under_title = tkinter.Frame(self.inner_frame_top_right, background = 'black', height = 5, bd = 0, highlightthickness = 0)
        block_under_title.pack(side = tkinter.BOTTOM, fill = 'x')
        label = tkinter.Label(self.inner_frame_top_right, text = 'CATAN', font = ('Arial', 20, 'bold'), background = self.BG_COLOR)
        label.pack(anchor = tkinter.S, side = tkinter.LEFT)
        label = tkinter.Label(self.inner_frame_top_right, text = 'SETTLING PHASE', font = ('Arial', 12), padx = 5, pady = 5, background = self.BG_COLOR)
        label.pack(anchor = tkinter.S, side = tkinter.LEFT)
        
    def setup_inner_frame_middle_left(self):
        self.canvas = tkinter.Canvas(self.inner_frame_middle_left, background = 'lightblue', bd = 0, highlightthickness = 0)
        self.canvas.pack(expand = True)
        self.hexagon_rendering = HexagonRendering(self)
    
    @abc.abstractmethod
    def setup_inner_frame_middle_right(self): ### Specific to settling phase (the rest isn't)
        pass
    
    def setup_inner_frame_bottom_left(self, instruction_text, label_bg_color):
        self.instruction_text = tkinter.StringVar()
        self.instruction_text.set(instruction_text)
        self.instruction = tkinter.Label(self.inner_frame_bottom_left, textvariable = self.instruction_text, background = label_bg_color, font = ('Arial, 12'), borderwidth = 1, relief = 'solid')
        self.instruction.place(anchor = tkinter.CENTER, relheight = 0.5, relwidth = 0.8, relx = 0.5, rely = 0.5)

    def setup_inner_frame_bottom_right(self):
        self.button_text = tkinter.StringVar()
        self.button_text.set('N/A')
        self.button = tkinter.Button(self.inner_frame_bottom_right, textvariable = self.button_text)
        self.button.place(anchor = tkinter.W, relheight = 0.5, relwidth = 0.5, relx = 0.5, rely = 0.5)
    
    def run(self):
        self.root.bind('<Configure>', self.hexagon_rendering.handle_resize)
        self.canvas.bind('<Motion>', lambda evt: self.hexagon_rendering.handle_motion(evt))
        self.canvas.bind('<Leave>', self.hexagon_rendering.unfocus_focused_hexagons)
        self.root.mainloop()
    
    def update_gui(self):
        instruction_text = "It's your turn!" if self.chaperone.player == self.chaperone.active_player else "Please wait for your turn!"
        self.instruction_text.set(instruction_text)