import tkinter

from frontend.ColorUtils import ColorUtils

class CardFrameLabel(tkinter.Label):
    def __init__(self, *args, **kwargs):
        self.enabled_background = kwargs.get('background')
        self.disabled_background = ColorUtils.desaturate_hex(self.enabled_background, 0.99)
        self.master = kwargs.get('master')
        kwargs['background'] = self.disabled_background ### To default to disabled background
        kwargs['foreground'] = ColorUtils.get_fg_from_bg(self.disabled_background, light_fg = '#DCDCDC', dark_fg = '#808080')
        super().__init__(*args, **kwargs)
    
    def enable(self):
        self.configure(
            background = self.enabled_background,
            foreground = ColorUtils.get_fg_from_bg(self.enabled_background)
        )
        self.master.configure(highlightbackground = '#000000')
    
    def disable(self):
        self.configure(
            background = self.disabled_background,
            foreground = ColorUtils.get_fg_from_bg(self.disabled_background, light_fg = '#DCDCDC', dark_fg = '#808080')
        )
        self.master.configure(highlightbackground = '#808080')