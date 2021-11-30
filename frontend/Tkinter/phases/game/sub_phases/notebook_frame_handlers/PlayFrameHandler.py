from collections import namedtuple
from functools import partial
import tkinter
from tkinter import ttk

from config import config
from frontend.ColorUtils import ColorUtils
from frontend.Tkinter.phases.Phase import Phase
from frontend.Tkinter.phases.game.sub_phases.notebook_frame_handlers.BaseFrameHandler import BaseFrameHandler
from frontend.Tkinter.phases.game.sub_phases.notebook_frame_handlers.CardFrame import CardFrame
from frontend.Tkinter.phases.game.sub_phases.notebook_frame_handlers.CardFrameLabel import CardFrameLabel

### TODO: factor out "darker_blue" stuff (and any instance of ColourUtils.darken_hex being used elsewhere)

class PlayFrameHandler(BaseFrameHandler):
    def setup(self):
        self.dice_roll_setup()

    def dice_roll_setup(self):
        darker_blue = ColorUtils.darken_hex(Phase.BG_COLOR, 0.2)
        self.dice_roll_container = tkinter.Frame(self.frame, background = darker_blue, height = 200, width = 300)

        self.dice_roll_text = tkinter.StringVar()
        self.dice_roll_text.set('')
        dice_roll_label = tkinter.Label(self.dice_roll_container, textvariable = self.dice_roll_text, background = darker_blue, font = ('Arial', 24))
        dice_roll_label.place(in_ = self.dice_roll_container, relx = 0.05, rely = 0.05)

        self.dice_roll_event_text = tkinter.StringVar()
        self.dice_roll_event_text.set('')
        dice_roll_event_label = tkinter.Label(self.dice_roll_container, textvariable = self.dice_roll_event_text, background = darker_blue, font = ('Arial', 12), justify = tkinter.LEFT, wraplength = 275)
        dice_roll_event_label.place(in_ = self.dice_roll_container, relx = 0.05, rely = 0.25)

        self.instruct_label_text = tkinter.StringVar()
        self.instruct_label_text.set('Roll dice')
        self.instruct_label = tkinter.Label(self.dice_roll_container, textvariable = self.instruct_label_text, background = Phase.BG_COLOR, padx = 10, pady = 10, font = ('Arial', 16, 'bold'))
        self.instruct_label.place(in_ = self.dice_roll_container, relx = 0.05, rely = 0.685)
        self.dice_roll_container.place(in_ = self.frame, anchor = tkinter.CENTER, relx = 0.5, rely = 0.5)
        self.instruct_label.bind('<Motion>', lambda evt: self.root.configure(cursor = Phase.CURSOR_HAND))
        self.instruct_label.bind('<Leave>', lambda evt: self.root.configure(cursor = Phase.CURSOR_DEFAULT))
        self.instruct_label.bind('<Button-1>', self.roll_dice)

    def transition_to_action_selection(self, event):
        self.dice_roll_container.destroy()
        self.action_selection_setup()
        self.action_tree.bind('<Motion>', self.action_tree_motion_handler)
        self.action_tree.bind('<Leave>', self.action_tree_leave_handler)
        
    def action_selection_setup(self):
        self.labels = []
        self.frame.grid_columnconfigure(0, weight = 1)
        self.card_frames = {}
        self.card_num_label_texts = {}
        self.resource_cards_frame = self.create_resource_cards_frame(self.frame)
        self.resource_cards_frame.grid(row = 0, column = 0, sticky = 'ew')
        self.development_card_frame = self.create_development_cards_frame(self.frame)
        self.development_card_frame.grid(row = 1, column = 0, sticky = 'ew')
        self.movable_piece_frame = self.create_movable_piece_frame(self.frame)
        self.movable_piece_frame.grid(row = 2, column = 0, sticky = 'ew')
        self.action_frame = self.create_action_frame(self.frame)
        self.action_cost_frame = self.create_action_cost_frame(self.frame)
        if self.phase.client_active():
            self.enable()
    
    def roll_dice(self, event):
        self.phase.chaperone.roll_dice()
    
    def enable(self):
        ### Probably don't actually want to enable / disable card frames just based on whether user is active - should be based on whether user has item
        for card_frames in self.card_frames.values():
            for card_frame in card_frames.values():
                card_frame.enable()
        self.action_frame.grid(row = 3, column = 0, sticky = 'ew')
        self.action_cost_frame.grid(row = 4, column = 0, sticky = 'ew')

    def disable(self):
        for card_frames in self.card_frames.values():
            for card_frame in card_frames.values():
                card_frame.disable()
        self.action_frame.grid_forget()

    def create_cards_frame(self, where, type, iterable):
        self.root.update_idletasks()
        frame_width = where.master.master.winfo_width() ### Get width of inner frame middle right
        darker_blue = ColorUtils.darken_hex(Phase.BG_COLOR, 0.2)
        outer_frame = tkinter.Frame(where, background = Phase.BG_COLOR, padx = 5, pady = 5)
        outer_frame_top = tkinter.Label(outer_frame, text = f'{type.title()} cards', anchor = tkinter.W, background = darker_blue)
        outer_frame_bottom = tkinter.Frame(outer_frame, background = darker_blue, pady = 5)
        outer_frame_top.pack(fill = 'x', side = tkinter.TOP)
        outer_frame_bottom.pack(fill = 'x', side = tkinter.TOP)
        outer_frame.grid_rowconfigure(0, weight = 1)
        self.card_frames[type] = {}
        self.card_num_label_texts[type] = {}
        for i, tup in enumerate(iterable):
            outer_frame_bottom.grid_columnconfigure(i, weight = 1, uniform = 'catan')
            inner_frame = CardFrame(outer_frame_bottom, highlightbackground = '#808080', highlightthickness = 3)
            self.card_frames[type][tup.name] = inner_frame
            type_label_text = tup.name.title().replace('_', ' ')
            label_partial = partial(CardFrameLabel, master = inner_frame, background = tup.color, width = round(frame_width / 50), wraplength = round(frame_width / 8))
            type_label = label_partial(height = 1, text = type_label_text)
            num_label_text = tkinter.StringVar()
            num_of_thing = self.phase.chaperone.player.num_of_resource_in_hand(tup.name)
            num_label_text.set(num_of_thing)
            self.card_num_label_texts[type][tup.name] = num_label_text
            num_label = label_partial(font = ('Arial', '12', 'bold'), height = 1, textvariable = num_label_text)
            type_label.pack(expand = True, fill = 'both', side = tkinter.TOP)
            num_label.pack(expand = True, fill = 'both', side = tkinter.TOP)
            self.labels.extend([type_label, num_label])
            inner_frame.grid(row = 0, column = i, padx = 2.5)
        return outer_frame
    
    def create_resource_cards_frame(self, where):
        iterable = [
            namedtuple('ResourceCard', ['name', 'color'])(k, v['color'])
            for k, v in config['resource_types'].items()
            if k != 'desert'
        ]
        return self.create_cards_frame(where, 'resource', iterable)
    
    def create_development_cards_frame(self, where):
        iterable = [
            namedtuple('DevelopmentCard', ['name', 'color'])(k, v['color'])
            for k, v in config['development_card_types'].items()
        ]
        return self.create_cards_frame(where, 'development', iterable)
    
    def create_movable_piece_frame(self, where):
        outer_frame = tkinter.Frame(where, background = Phase.BG_COLOR, padx = 5, pady = 5)
        darker_blue = ColorUtils.darken_hex(Phase.BG_COLOR, 0.2)
        inner_frame = tkinter.Frame(outer_frame, background = darker_blue)
        inner_frame.pack(fill = 'x', side = tkinter.TOP)
        for i, movable_pieces in enumerate(['roads', 'settlements', 'cities', 'tokens']): ### Only add tokens if two players
            piece_label = tkinter.Label(inner_frame, text = f'{movable_pieces.title()}:', background = darker_blue)
            piece_label.grid(row = 0, column = i * 2)
            num_label_text = tkinter.StringVar() ### Needs to be accessible later
            num_label_text.set(str(len(getattr(self.player, movable_pieces, []))))
            num_label = tkinter.Label(inner_frame, textvariable = num_label_text, background = darker_blue)
            num_label.grid(row = 0, column = i * 2 + 1)
        return outer_frame
    
    def create_action_frame(self, where):
        outer_frame = tkinter.Frame(where, background = Phase.BG_COLOR, padx = 5, pady = 5)
        darker_blue = ColorUtils.darken_hex(Phase.BG_COLOR, 0.2)
        inner_frame = tkinter.Frame(outer_frame, background = darker_blue, padx = 5, pady = 5)
        inner_frame.pack(side = tkinter.TOP, expand = True, fill = 'both')
        self.action_tree = ttk.Treeview(inner_frame, columns = ['action'], show = 'headings', height = 5)
        self.action_tree.tag_configure('odd', background = Phase.BG_COLOR)
        self.action_tree.tag_configure('even', background = ColorUtils.darken_hex(Phase.BG_COLOR, 0.05))
        self.action_tree.tag_configure('disabled', foreground = 'grey')
        self.action_tree.tag_configure('enabled', foreground = 'black')
        self.action_tree.heading('action', text = 'Action', anchor = tkinter.W)
        self.fill_action_tree()
        self.action_tree.pack(expand = True, fill = 'x', side = tkinter.LEFT)
        scrollbar = ttk.Scrollbar(inner_frame, orient = tkinter.VERTICAL, command = self.action_tree.yview, style = 'My.Vertical.TScrollbar')
        self.action_tree.configure(yscrollcommand = scrollbar.set)
        scrollbar.pack(fill = 'y', side = tkinter.LEFT)
        return outer_frame
    
    def create_action_cost_frame(self, where):
        outer_frame = tkinter.Frame(where, background = Phase.BG_COLOR, padx = 5, pady = 5)
        darker_blue = ColorUtils.darken_hex(Phase.BG_COLOR, 0.2)
        inner_frame = tkinter.Frame(outer_frame, background = darker_blue, padx = 5, pady = 5)
        inner_frame.pack(side = tkinter.TOP, expand = True, fill = 'both')
        self.action_cost = tkinter.StringVar()
        self.action_cost.set(self.default_action_cost_text())
        darker_blue = ColorUtils.darken_hex(Phase.BG_COLOR, 0.2)
        cost_label = tkinter.Label(inner_frame, textvariable = self.action_cost, background = darker_blue)
        cost_label.pack()
        return outer_frame
    
    def fill_action_tree(self):
        self.action_tree.delete(*self.action_tree.get_children())
        for i, (action_const, action_data) in enumerate(config['actions'].items()):
            even_tag = 'even' if i % 2 == 0 else 'odd'
            enabled_tag = 'enabled' if self.player.can_afford(action_const) else 'disabled'
            self.action_tree.insert('', tkinter.END, iid = action_const, text = action_const, values = (action_data['name'],), tags = (even_tag, enabled_tag))
    
    def action_tree_motion_handler(self, event):
        item = self.action_tree.identify('item', event.x, event.y)
        item = self.action_tree.item(item)
        action, tags = item['text'], item['tags']
        self.root.configure({'cursor': Phase.CURSOR_HAND if 'enabled' in tags else Phase.CURSOR_DEFAULT})
        self.show_action_cost(action)
        # self.action_tree.item(action, tags = ('enabled'))
    
    def action_tree_leave_handler(self, event):
        self.root.configure({'cursor': Phase.CURSOR_DEFAULT})
        self.action_cost.set(self.default_action_cost_text())
    
    def show_action_cost(self, action):
        if action:
            action_config = config['actions'][action]
            cost_text = ' | '.join([f'{k.title().replace("_", " ")} - {v}' for v in action_config['cost'].values() for k, v in v.items()])
            cost_text = f'Cost: {cost_text}'
        else:
            cost_text = self.default_action_cost_text()
        self.action_cost.set(cost_text)
    
    def default_action_cost_text(self):
        return 'Hover over an action to see how much it costs!'