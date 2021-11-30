import tkinter

class CardFrame(tkinter.Frame):
    def enable_or_disable_cards(self, event = None):
        children = self.winfo_children()
        num_label = children[-1]
        enable = int(num_label.cget('text')) > 0
        for child in children:
            if enable:
                child.enable()
            else:
                child.disable()