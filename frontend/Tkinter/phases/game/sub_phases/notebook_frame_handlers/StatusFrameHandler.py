import tkinter
from frontend.Tkinter.phases.game.sub_phases.notebook_frame_handlers.BaseFrameHandler import BaseFrameHandler

class StatusFrameHandler(BaseFrameHandler):
    def setup(self):
        self.text_variable = tkinter.StringVar()
        self.text_variable.set('')
        self.text_box = tkinter.Label(self.frame, textvariable = self.text_variable)
        self.text_box.pack(expand = True, fill = 'both', padx = 5, pady = 5)