import tkinter

class CardFrame(tkinter.Frame):
    def enable(self, event = None):
        for child in self.winfo_children():
            child.enable()
    
    def disable(self, event = None):
        for child in self.winfo_children():
            child.disable()