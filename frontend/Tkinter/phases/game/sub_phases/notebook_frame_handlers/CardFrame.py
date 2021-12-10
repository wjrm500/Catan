import tkinter

class CardFrame(tkinter.Frame):
    def highlight_or_unhighlight_labels(self, event = None):
        children = self.winfo_children()
        num_label = children[-1]
        highlight = int(num_label.cget('text')) > 0
        if highlight:
            self.highlight_labels()
        else:
            self.unhighlight_labels()
    
    def highlight_labels(self):
        children = self.winfo_children()
        for child in children:
            child.highlight()

    def unhighlight_labels(self):
        children = self.winfo_children()
        for child in children:
            child.unhighlight()
        
    def make_labels_clickable(self, event_handler):
        children = self.winfo_children()
        for child in children:
            child.make_clickable(event_handler)
        
    def make_labels_unclickable(self):
        children = self.winfo_children()
        for child in children:
            child.make_unclickable()
    
    def get_type(self):
        children = self.winfo_children()
        type_label = children[0]
        return type_label.cget('text').lower().replace(' ', '_')