from collections import namedtuple
from functools import partial
import tkinter
from tkinter import ttk

from config import config
from frontend.ColorUtils import ColorUtils
from frontend.Tkinter.phases.Phase import Phase
from frontend.Tkinter.phases.game.sub_phases.notebook_frame_handlers.BaseFrameHandler import BaseFrameHandler

class PlayFrameHandler(BaseFrameHandler):
    def setup(self):
        self.labels = []
        self.frame.grid_columnconfigure(0, weight = 1)
        self.resource_card_frame = self.create_resource_card_frame(self.frame)
        self.resource_card_frame.grid(row = 0, column = 0, sticky = 'ew')
        self.development_card_frame = self.create_development_card_frame(self.frame)
        self.development_card_frame.grid(row = 1, column = 0, sticky = 'ew')
        self.movable_piece_frame = self.create_movable_piece_frame(self.frame)
        self.movable_piece_frame.grid(row = 2, column = 0, sticky = 'ew')
        self.action_frame = self.create_action_frame(self.frame)
        self.action_frame.grid(row = 3, column = 0, sticky = 'ew')
        self.frame.grid_rowconfigure(3, weight = 1)

    def create_card_frame(self, where, title, iterable):
        self.root.update_idletasks()
        frame_width = where.master.master.winfo_width() ### Get width of inner frame middle right
        darker_blue = ColorUtils.darken_hex(Phase.BG_COLOR, 0.2)
        outer_frame = tkinter.Frame(where, background = Phase.BG_COLOR, padx = 5, pady = 5)
        outer_frame_top = tkinter.Label(outer_frame, text = title, anchor = tkinter.W, background = darker_blue)
        outer_frame_bottom = tkinter.Frame(outer_frame, background = darker_blue, pady = 5)
        outer_frame_top.pack(fill = 'x', side = tkinter.TOP)
        outer_frame_bottom.pack(side = tkinter.TOP)
        outer_frame.grid_rowconfigure(0, weight = 1)
        for i, tup in enumerate(iterable):
            outer_frame_bottom.grid_columnconfigure(i, weight = 1, uniform = 'catan')
            inner_frame = tkinter.Frame(outer_frame_bottom, background = tup.color, highlightbackground = 'black', highlightthickness = 3)
            type_label_text = tup.name.title().replace('_', ' ')
            label_partial = partial(tkinter.Label, inner_frame, background = tup.color, foreground = ColorUtils.get_fg_from_bg(tup.color), width = round(frame_width / 50), wraplength = round(frame_width / 8))
            type_label = label_partial(height = 1, text = type_label_text)
            num_label_text = tkinter.StringVar() ### Needs to be accessible later
            num_label_text.set('0')
            num_label = label_partial(font = ('Arial', '12', 'bold'), height = 1, textvariable = num_label_text)
            type_label.pack(expand = True, fill = 'both', side = tkinter.TOP)
            num_label.pack(expand = True, fill = 'both', side = tkinter.TOP)
            self.labels.extend([type_label, num_label])
            inner_frame.grid(row = 0, column = i, padx = 2.5)
        return outer_frame
    
    def create_resource_card_frame(self, where):
        iterable = [
            namedtuple('ResourceCard', ['name', 'color'])(k, v['color'])
            for k, v in config['resource_types'].items()
            if k != 'desert'
        ]
        return self.create_card_frame(where, 'Resource cards', iterable)
    
    def create_development_card_frame(self, where):
        iterable = [
            namedtuple('DevelopmentCard', ['name', 'color'])(k, v['color'])
            for k, v in config['development_card_types'].items()
        ]
        return self.create_card_frame(where, 'Development cards', iterable)
    
    def create_movable_piece_frame(self, where):
        outer_frame = tkinter.Frame(where, background = Phase.BG_COLOR, padx = 5, pady = 5)
        darker_blue = ColorUtils.darken_hex(Phase.BG_COLOR, 0.2)
        inner_frame = tkinter.Frame(outer_frame, background = darker_blue)
        inner_frame.pack(fill = 'x', side = tkinter.TOP)
        for i, movable_pieces in enumerate(['roads', 'settlements', 'cities', 'tokens']): ### Only add tokens if two players
            piece_label = tkinter.Label(inner_frame, text = f'{movable_pieces.title()}:', background = darker_blue)
            piece_label.grid(row = 0, column = i * 2)
            num_label_text = tkinter.StringVar() ### Needs to be accessible later
            num_label_text.set('0')
            num_label = tkinter.Label(inner_frame, textvariable = num_label_text, background = darker_blue)
            num_label.grid(row = 0, column = i * 2 + 1)
        return outer_frame
    
    def create_action_frame(self, where):
        outer_frame = tkinter.Frame(where, background = Phase.BG_COLOR, padx = 5, pady = 5)
        darker_blue = ColorUtils.darken_hex(Phase.BG_COLOR, 0.2)
        inner_frame = tkinter.Frame(outer_frame, background = darker_blue, padx = 5, pady = 5)
        inner_frame.pack(side = tkinter.TOP, expand = True, fill = 'both')
        columns = ['action', 'cost']
        self.action_tree = ttk.Treeview(inner_frame, columns = columns, show = 'headings')
        self.action_tree.tag_configure('odd', background = Phase.BG_COLOR)
        self.action_tree.tag_configure('even', background = ColorUtils.darken_hex(Phase.BG_COLOR, 0.05))
        self.action_tree.tag_configure('disabled', foreground = 'grey')
        self.action_tree.tag_configure('enabled', foreground = 'black')
        self.action_tree.column('#1', width = 180, stretch = False)
        self.action_tree.heading('action', text = 'Action', anchor = tkinter.W)
        self.action_tree.heading('cost', text = 'Cost', anchor = tkinter.W)
        for i, action in enumerate(config['actions']):
            cost_text = ' | '.join([f'{k.title().replace("_", " ")} - {v}' for v in action['cost'].values() for k, v in v.items()])
            self.action_tree.insert('', tkinter.END, iid = action['const'], text = action['const'], values = (action['name'], cost_text), tags = ('even' if i % 2 == 0 else 'odd', 'disabled' if i > 0 else 'enabled'))
        self.action_tree.pack(expand = True, fill = 'x', side = tkinter.LEFT)
        scrollbar = ttk.Scrollbar(inner_frame, orient = tkinter.VERTICAL, command = self.action_tree.yview, style = 'My.Vertical.TScrollbar')
        self.action_tree.configure(yscrollcommand = scrollbar.set)
        scrollbar.pack(fill = 'y', side = tkinter.LEFT)
        return outer_frame
    
    def motion_handler(self, event):
        item = self.action_tree.identify('item', event.x, event.y)
        item = self.action_tree.item(item)
        action, tags = item['text'], item['tags']
        self.root.configure({'cursor': Phase.CURSOR_HAND if 'enabled' in tags else Phase.CURSOR_DEFAULT})
        # self.action_tree.item(action, tags = ('enabled'))