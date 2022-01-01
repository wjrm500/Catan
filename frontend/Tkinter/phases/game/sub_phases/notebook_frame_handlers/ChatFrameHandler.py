import tkinter
from frontend.ColorUtils import ColorUtils
from frontend.EntryWithPlaceholder import EntryWithPlaceholder
from frontend.Tkinter.phases.Phase import Phase

from frontend.Tkinter.phases.game.sub_phases.notebook_frame_handlers.BaseFrameHandler import BaseFrameHandler

class ChatFrameHandler(BaseFrameHandler):
    def __init__(self, phase, notebook) -> None:
        super().__init__(phase, notebook)
        self.text_inserted = False

    def setup(self):
        self.text_area = tkinter.scrolledtext.ScrolledText(self.frame, font = ('Arial', 12), padx = 10, pady = 10, wrap = 'word', background = ColorUtils.lighten_hex(Phase.BG_COLOR, 0.2))
        self.text_area.config(state = 'disabled')
        self.frame.grid_columnconfigure(0, weight = 1)
        self.text_area.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'ew')
        self.frame.grid_rowconfigure(0, weight = 1, uniform = 'catan')
        self.text_entry = EntryWithPlaceholder(self.frame, placeholder = 'Type your message here and hit enter to send!', font = ('Arial', 12))
        self.text_entry.grid(row = 1, column = 0, sticky = 'ew', padx = 5, pady = 5, ipadx = 3, ipady = 3)
        self.frame.grid_rowconfigure(1, weight = 1)
        self.text_entry.bind('<Return>', self.send_chat_message)

        for player in self.player.game.players:
            self.text_area.tag_config(f'{player.name}_font', foreground = player.color, font = ('Arial', 12, 'bold'))
        self.text_area.tag_config('datetime_font', foreground = 'gray', font = ('Arial', 12))
    
    def send_chat_message(self, event):
        text = self.text_entry.get()
        self.phase.chaperone.send_chat_message(text)
        self.text_entry.delete(0, tkinter.END)