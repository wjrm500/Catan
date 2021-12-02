import tkinter
from frontend.ColorUtils import ColorUtils
from frontend.Tkinter.phases.Phase import Phase

from frontend.Tkinter.phases.game.sub_phases.notebook_frame_handlers.BaseFrameHandler import BaseFrameHandler

class HistoryFrameHandler(BaseFrameHandler):
    def setup(self):
        self.text_area = tkinter.scrolledtext.ScrolledText(self.frame, font = ('Arial', 12), padx = 10, pady = 10, wrap = 'word', background = ColorUtils.lighten_hex(Phase.BG_COLOR, 0.2))
        self.text_area.config(state = 'normal')
        self.text_area.insert('end', self.phase.chaperone.settling_phase_text)
        self.text_area.yview('end')
        self.text_area.config(state = 'disabled')
        self.text_area.place(in_ = self.frame, anchor = tkinter.CENTER, relx = 0.5, rely = 0.5, relwidth = 1, relheight = 1)