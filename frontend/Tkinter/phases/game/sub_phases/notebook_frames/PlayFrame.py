import tkinter

from config import config
from frontend.Tkinter.phases.game.sub_phases.notebook_frames.BaseFrame import BaseFrame

class PlayFrame(BaseFrame):
    def setup(self):
        resource_card_frame = self.resource_card_frame(self.frame)
        resource_card_frame.pack(side = tkinter.TOP)
    
    def resource_card_frame(self, where):
        outer_frame = tkinter.Frame(where)
        for resource_type, data in config['resource_types'].items():
            if resource_type == 'desert':
                continue
            inner_frame = tkinter.Frame(outer_frame, background = data['color'])
            label = tkinter.Label(inner_frame, text = resource_type.title(), background = data['color'])
            label.pack(expand = True, fill = 'both')
            inner_frame.pack(side = tkinter.LEFT)
        return outer_frame