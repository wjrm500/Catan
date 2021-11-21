from collections import namedtuple
from functools import partial
import tkinter

from config import config
from frontend.ColorUtils import ColorUtils
from frontend.Tkinter.phases.game.sub_phases.notebook_frame_handlers.BaseFrameHandler import BaseFrameHandler

class PlayFrameHandler(BaseFrameHandler):
    def setup(self):
        self.labels = []
        resource_card_frame = self.resource_card_frame(self.frame)
        resource_card_frame.pack(side = tkinter.TOP)
        development_card_frame = self.development_card_frame(self.frame)
        development_card_frame.pack(side = tkinter.TOP)
    
    def card_frame(self, where, iterable):
        self.root.update_idletasks()
        frame_height = where.master.master.winfo_height() ### Get height of inner frame middle right
        frame_width = where.master.master.winfo_width() ### Get width of inner frame middle right
        outer_frame = tkinter.Frame(where, pady = 10)
        outer_frame.grid_rowconfigure(0, weight = 1)
        for i, tup in enumerate(iterable):
            outer_frame.grid_columnconfigure(i, weight = 1, uniform = 'catan')
            inner_frame = tkinter.Frame(outer_frame, background = tup.color, highlightbackground = 'black', highlightthickness = 3)
            type_label_text = tup.name.title().replace('_', ' ')
            label_partial = partial(tkinter.Label, inner_frame, background = tup.color, foreground = ColorUtils.get_fg_from_bg(tup.color), width = round(frame_width / 50), wraplength = round(frame_width / 8))
            type_label = label_partial(height = 2, text = type_label_text)
            num_label_text = tkinter.StringVar() ### Needs to be accessible later
            num_label_text.set('0')
            num_label = label_partial(font = ('Arial', '12'), height = 1, textvariable = num_label_text)
            type_label.pack(expand = True, fill = 'both', side = tkinter.TOP)
            num_label.pack(expand = True, fill = 'both', side = tkinter.TOP)
            self.labels.extend([type_label, num_label])
            inner_frame.grid(row = 0, column = i, padx = 10)
        return outer_frame
    
    def resource_card_frame(self, where):
        iterable = [
            namedtuple('ResourceCard', ['name', 'color'])(k, v['color'])
            for k, v in config['resource_types'].items()
            if k != 'desert'
        ]
        return self.card_frame(where, iterable)
    
    def development_card_frame(self, where):
        iterable = [
            namedtuple('DevelopmentCard', ['name', 'color'])(k, v['color'])
            for k, v in config['development_card_types'].items()
        ]
        return self.card_frame(where, iterable)