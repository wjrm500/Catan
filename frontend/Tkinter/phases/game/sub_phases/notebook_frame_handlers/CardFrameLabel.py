import tkinter

from frontend.ColorUtils import ColorUtils
from frontend.Tkinter.phases.Phase import Phase

class CardFrameLabel(tkinter.Label):
    def __init__(self, *args, **kwargs):
        self.enabled_background = kwargs.get('background')
        self.disabled_background = ColorUtils.desaturate_hex(self.enabled_background, 0.99)
        self.master = kwargs.get('master')
        kwargs['background'] = self.disabled_background ### To default to disabled background
        kwargs['foreground'] = ColorUtils.get_fg_from_bg(self.disabled_background, light_fg = '#DCDCDC', dark_fg = '#808080')
        super().__init__(*args, **kwargs)
    
    def enable(self, clickable, event_handler):
        self.configure(
            background = self.enabled_background,
            foreground = ColorUtils.get_fg_from_bg(self.enabled_background)
        )
        self.master.configure(highlightbackground = '#000000')
        if clickable:
            root = self.winfo_toplevel()
            self.bind('<Button-1>', event_handler)
            self.bind('<Motion>', lambda evt: root.configure(cursor = Phase.CURSOR_HAND))
            self.bind('<Leave>', lambda evt: root.configure(cursor = Phase.CURSOR_DEFAULT))
    
    def disable(self):
        self.configure(
            background = self.disabled_background,
            foreground = ColorUtils.get_fg_from_bg(self.disabled_background, light_fg = '#DCDCDC', dark_fg = '#808080')
        )
        self.master.configure(highlightbackground = '#808080')
    
    def make_unclickable(self):
        self.unbind('<Button-1>')
        self.unbind('<Motion>')
        self.unbind('<Leave>')