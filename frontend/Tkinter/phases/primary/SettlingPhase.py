import tkinter
import tkinter.scrolledtext
import textwrap
from frontend.ColorUtils import ColorUtils
from frontend.Tkinter.phases.Phase import Phase
from frontend.Tkinter.rendering.HexagonRendering import HexagonRendering
from functools import partial

class SettlingPhase(Phase):
    def __init__(self, chaperone):
        super().__init__(chaperone)
        self.root.geometry('1000x500')
        self.frames = []
        standard_frame = partial(tkinter.Frame, background = self.BG_COLOR)#, highlightbackground = ColorUtils.darken_hex(self.BG_COLOR, 0.03), highlightthickness = 1)
        self.inner_frame = standard_frame(self.root)
        self.inner_frame.pack(fill = 'both', expand = True, padx = 10, pady = 10)
        inner_frame_top = standard_frame(self.inner_frame, height = 50)
        inner_frame_top.pack(side = tkinter.TOP, fill = 'x')
        inner_frame_top_left = standard_frame(inner_frame_top, height = 50)
        inner_frame_top_right = standard_frame(inner_frame_top, height = 50)
        inner_frame_top_left.place(in_ = inner_frame_top, anchor = 'e', relheight = 1.0, relwidth = 0.5, relx = 0.5, rely = 0.5)
        inner_frame_top_right.place(in_ = inner_frame_top, anchor = 'w', relheight = 1.0, relwidth = 0.5, relx = 0.5, rely = 0.5)
        inner_frame_middle = standard_frame(self.inner_frame)
        inner_frame_middle.pack(side = tkinter.TOP, fill = 'both', expand = True)
        inner_frame_middle_left = standard_frame(inner_frame_middle)
        inner_frame_middle_right = standard_frame(inner_frame_middle)
        inner_frame_middle_left.place(in_ = inner_frame_middle, anchor = 'e', relheight = 1.0, relwidth = 0.5, relx = 0.5, rely = 0.5)
        inner_frame_middle_right.place(in_ = inner_frame_middle, anchor = 'w', relheight = 1.0, relwidth = 0.5, relx = 0.5, rely = 0.5)
        inner_frame_bottom = standard_frame(self.inner_frame, height = 50)
        inner_frame_bottom.pack(side = tkinter.BOTTOM, fill = 'x')
        inner_frame_bottom_left = standard_frame(inner_frame_bottom, height = 50)
        inner_frame_bottom_right = standard_frame(inner_frame_bottom, height = 50, padx = 10)
        inner_frame_bottom_left.place(in_ = inner_frame_bottom, anchor = 'e', relheight = 1.0, relwidth = 0.5, relx = 0.5, rely = 0.5)
        inner_frame_bottom_right.place(in_ = inner_frame_bottom, anchor = 'w', relheight = 1.0, relwidth = 0.5, relx = 0.5, rely = 0.5)
        
        self.canvas = tkinter.Canvas(inner_frame_middle_left, background = 'lightblue', bd = 0, highlightthickness = 0)
        self.canvas.pack(expand = True)
        self.hexagon_rendering = HexagonRendering(self)

        block_under_title = tkinter.Frame(inner_frame_top_right, background = 'black', height = 5, bd = 0, highlightthickness = 0)
        block_under_title.pack(side = tkinter.BOTTOM, fill = 'x')
        label = tkinter.Label(inner_frame_top_right, text = 'CATAN', font = ('Arial', 20, 'bold'), background = self.BG_COLOR)
        label.pack(anchor = tkinter.S, side = tkinter.LEFT)
        label = tkinter.Label(inner_frame_top_right, text = 'SETTLING PHASE', font = ('Arial', 12), padx = 5, pady = 5, background = self.BG_COLOR)
        label.pack(anchor = tkinter.S, side = tkinter.LEFT)
        
        ### Specific to settling phase (the rest isn't)
        self.text_area = tkinter.scrolledtext.ScrolledText(inner_frame_middle_right, font = ('Arial', 12), padx = 10, wrap = 'word', background = ColorUtils.lighten_hex(self.BG_COLOR, 0.2))
        self.text_area.pack(padx = 10, pady = 10)
        self.text_area.config(state = 'normal')
        self.text_area.insert('end', self.get_introductory_text())
        self.text_area.yview('end')
        self.text_area.config(state = 'disabled')
        
        self.instruction_text = tkinter.StringVar()
        self.instruction_text.set('Awaiting instruction...')
        self.instruction = tkinter.Label(inner_frame_bottom_left, textvariable = self.instruction_text)
        self.instruction.place(anchor = tkinter.CENTER, relheight = 0.5, relwidth = 0.8, relx = 0.5, rely = 0.5)

        self.button_text = tkinter.StringVar()
        self.button_text.set('N/A')
        self.button = tkinter.Button(inner_frame_bottom_right, textvariable = self.button_text)
        self.button.place(anchor = tkinter.W, relheight = 0.5, relwidth = 0.5, relx = 0.5, rely = 0.5)
    
    def run(self):
        self.root.bind('<Configure>', self.hexagon_rendering.handle_resize)
        self.canvas.bind('<Motion>', lambda evt: self.hexagon_rendering.handle_motion(evt))
        self.canvas.bind('<Leave>', self.hexagon_rendering.unfocus_focused_hexagons)
        self.root.mainloop()
    
    def get_introductory_text(self):
        return textwrap.dedent("""
            Welcome to Catan!

            A game of Catan begins with each player placing settlements on two nodes, with a single road leading away from each settlement.

            Players take it in turns to place settlements and roads, with turn-taking following the “snake draft” format, such that the player who settles first will be the player who settles last.

            Players are ordered randomly for the first round of settling.
        """)