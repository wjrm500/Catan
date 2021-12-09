import tkinter

class CardFrame(tkinter.Frame):
    def enable_or_disable_labels(self, event = None, clickable = False, event_handler = None):
        children = self.winfo_children()
        num_label = children[-1]
        enable = int(num_label.cget('text')) > 0
        if enable:
            self.enable_labels(clickable, event_handler)
        else:
            self.disable_labels()
    
    def enable_labels(self, clickable = False, event_handler = None):
        children = self.winfo_children()
        for child in children:
            child.enable(clickable, event_handler)

    def disable_labels(self):
        children = self.winfo_children()
        for child in children:
            child.disable()
    
    def get_type(self):
        children = self.winfo_children()
        type_label = children[0]
        return type_label.cget('text').lower().replace(' ', '_')