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
        self.place_widget = lambda what, where, anchor: what.place(in_ = where, anchor = anchor, relheight = 1.0, relwidth = 0.5, relx = 0.5, rely = 0.5)
        self.active_player_index = 0
        self.setup_frames()
        self.setup_inner_frame_top_right()
        self.setup_inner_frame_middle_left()
        self.setup_inner_frame_middle_right()
        self.setup_inner_frame_bottom_left()
        self.setup_inner_frame_bottom_right()
    
    @abc.abstractmethod
    def update_active_player_index(self):
        pass

    def active_player(self):
        return self.chaperone.players[self.active_player_index]
    
    def client_active(self):
        return self.chaperone.player.id == self.active_player().id
    
    def setup_frames(self):
        frame_partial = partial(tkinter.Frame, background = self.BG_COLOR)#, highlightbackground = ColorUtils.darken_hex(self.BG_COLOR, 0.5), highlightthickness = 1)

        """
        Level 1 frames
        """
        self.inner_frame = frame_partial(self.root)
        self.inner_frame.pack(fill = 'both', expand = True, padx = 10, pady = 10)

        """
        Level 2 frames
        """
        # Top
        self.inner_frame_top = frame_partial(self.inner_frame, height = 50)
        self.inner_frame_top.pack(side = tkinter.TOP, fill = 'x')

        # Middle
        self.inner_frame_middle = frame_partial(self.inner_frame)
        self.inner_frame_middle.pack(side = tkinter.TOP, fill = 'both', expand = True)

        # Bottom
        self.inner_frame_bottom = frame_partial(self.inner_frame, height = 50)
        self.inner_frame_bottom.pack(side = tkinter.BOTTOM, fill = 'x')

        """
        Level 3 frames
        """
        # Top
        self.inner_frame_top_left = frame_partial(self.inner_frame_top, height = 50)
        self.place_widget(self.inner_frame_top_left, where = self.inner_frame_top, anchor = tkinter.E)
        self.inner_frame_top_right = frame_partial(self.inner_frame_top, height = 50)
        self.place_widget(self.inner_frame_top_right, where = self.inner_frame_top, anchor = tkinter.W)
        
        #  Middle
        self.inner_frame_middle_left = frame_partial(self.inner_frame_middle)
        self.place_widget(self.inner_frame_middle_left, where = self.inner_frame_middle, anchor = tkinter.E)
        self.inner_frame_middle_right = frame_partial(self.inner_frame_middle)
        self.place_widget(self.inner_frame_middle_right, where = self.inner_frame_middle, anchor = tkinter.W)
        
        # Bottom
        self.inner_frame_bottom_left = frame_partial(self.inner_frame_bottom, height = 50, padx = 10, pady = 5)
        self.place_widget(self.inner_frame_bottom_left, where = self.inner_frame_bottom, anchor = tkinter.E)
        self.inner_frame_bottom_right = frame_partial(self.inner_frame_bottom, height = 50, padx = 10, pady = 5)
        self.place_widget(self.inner_frame_bottom_right, where = self.inner_frame_bottom, anchor = tkinter.W)
    
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
        self.hexagon_rendering.canvas_mode = HexagonRendering.CANVAS_MODE_BUILD_SETTLEMENT if self.client_active() else HexagonRendering.CANVAS_MODE_DISABLED
    
    @abc.abstractmethod
    def setup_inner_frame_middle_right(self): ### Specific to settling phase (the rest isn't)
        pass
    
    def setup_inner_frame_bottom_left(self, instruction_text, label_bg_color):
        label_partial = partial(tkinter.Label, self.inner_frame_bottom_left, borderwidth = 1, font = ('Arial, 10'), padx = 5, pady = 5, relief = 'solid')

        self.inner_frame_bottom_left.grid_rowconfigure(0, weight = 1)
        self.inner_frame_bottom_left.grid_columnconfigure(0, weight = 1)
        self.inner_frame_bottom_left.grid_columnconfigure(1, weight = 1)

        self.root.update_idletasks()
        frame_width = self.inner_frame_bottom_left.winfo_width()

        self.instruction_text = tkinter.StringVar()
        self.instruction_text.set(instruction_text)
        self.instruction = label_partial(textvariable = self.instruction_text, background = label_bg_color, width = round(frame_width / 3))
        self.instruction.grid(row = 0, column = 0, padx = 10)

        player_data_text = f'Your color is {self.chaperone.player.color.upper()}'
        player_data = label_partial(text = player_data_text, background = self.chaperone.player.color, width = round(frame_width / 3))
        player_data.grid(row = 0, column = 1, padx = 10)

    def setup_inner_frame_bottom_right(self):
        self.button_text = tkinter.StringVar()
        self.button_text.set('N/A')
        self.button = tkinter.Button(self.inner_frame_bottom_right, textvariable = self.button_text)
        self.button.place(anchor = tkinter.W, relheight = 0.75, relwidth = 0.5, relx = 0.5, rely = 0.5)
    
    def run(self):
        self.root.bind('<Configure>', self.hexagon_rendering.handle_resize)
        self.canvas.bind('<Motion>', lambda evt: self.hexagon_rendering.handle_motion(evt))
        self.canvas.bind('<Leave>', self.hexagon_rendering.handle_leave)
        self.root.mainloop()        