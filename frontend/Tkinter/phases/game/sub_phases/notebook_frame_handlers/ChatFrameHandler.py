import tkinter
from frontend.ColorUtils import ColorUtils
from frontend.EntryWithPlaceholder import EntryWithPlaceholder
from frontend.Tkinter.phases.Phase import Phase

from frontend.Tkinter.phases.game.sub_phases.notebook_frame_handlers.BaseFrameHandler import BaseFrameHandler

class ChatFrameHandler(BaseFrameHandler):
    def setup(self):
        self.text_area = tkinter.scrolledtext.ScrolledText(self.frame, font = ('Arial', 12), padx = 10, pady = 10, wrap = 'word', background = ColorUtils.lighten_hex(Phase.BG_COLOR, 0.2))
        self.text_area.config(state = 'disabled')
        self.text_area.pack(expand = True, fill = 'both', padx = 5, pady = 5)
        self.text_entry = EntryWithPlaceholder(self.frame, placeholder = 'Type message here and hit enter to send!')
        self.text_entry.pack(expand = True, fill = 'both', padx = 5, pady = 5)
        self.text_entry.bind('<Return>', self.send_chat_message)
    
    def send_chat_message(self, event):
        text = self.text_entry.get()
        self.phase.chaperone.send_chat_message(text)
        self.text_entry.delete(0, tkinter.END)