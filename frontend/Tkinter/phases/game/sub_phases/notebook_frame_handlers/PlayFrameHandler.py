from collections import Counter, namedtuple
from functools import partial
import tkinter

from config import config
from frontend.Tkinter.phases.Phase import Phase
from frontend.Tkinter.phases.game.sub_phases.notebook_frame_handlers.ActionTreeHandler import ActionTreeHandler
from frontend.Tkinter.phases.game.sub_phases.notebook_frame_handlers.BaseFrameHandler import BaseFrameHandler
from frontend.Tkinter.phases.game.sub_phases.notebook_frame_handlers.CardFrame import CardFrame
from frontend.Tkinter.phases.game.sub_phases.notebook_frame_handlers.CardFrameLabel import CardFrameLabel

class PlayFrameHandler(BaseFrameHandler):
    def __init__(self, phase, notebook):
        super().__init__(phase, notebook)
        self.action_tree_handler = ActionTreeHandler(self)

    def setup(self):
        self.action_selection_setup()
        if self.phase.client_active():
            self.dice_roll_setup()
    
    def start_turn(self):
        self.dice_roll_setup()
    
    def transition_to_action_selection(self, event):
        self.root.configure(cursor = Phase.CURSOR_DEFAULT)
        self.dice_roll_overlay.destroy()
        self.update_resource_cards()
        self.update_movable_pieces()
        self.action_tree_handler.fill_action_tree()
        self.show_action_frame()
    
    def end_turn(self):
        self.hide_action_frame()

    def dice_roll_setup(self):
        self.dice_rolled = 0
        self.dice_roll_overlay = tkinter.Frame(self.frame, background = Phase.BG_COLOR)
        self.dice_roll_overlay.place(in_ = self.frame, anchor = tkinter.CENTER, relheight = 1, relwidth = 1, relx = 0.5, rely = 0.5)

        self.dice_roll_box = tkinter.Frame(self.dice_roll_overlay, background = Phase.DARKER_BG_COLOR, height = 250, width = 300)
        self.dice_roll_box.place(in_ = self.dice_roll_overlay, anchor = tkinter.CENTER, relx = 0.5, rely = 0.5)

        self.dice_roll_text = tkinter.StringVar()
        self.dice_roll_text.set('')
        dice_roll_label = tkinter.Label(self.dice_roll_box, textvariable = self.dice_roll_text, background = Phase.DARKER_BG_COLOR, font = ('Arial', 24))
        dice_roll_label.place(in_ = self.dice_roll_box, relx = 0.05, rely = 0.05)

        self.dice_roll_event_text = tkinter.StringVar()
        self.dice_roll_event_text.set('')
        dice_roll_event_label = tkinter.Label(self.dice_roll_box, textvariable = self.dice_roll_event_text, background = Phase.DARKER_BG_COLOR, font = ('Arial', 11), justify = tkinter.LEFT, wraplength = 275)
        dice_roll_event_label.place(in_ = self.dice_roll_box, relx = 0.05, rely = 0.25)

        self.instruct_label_text = tkinter.StringVar()
        self.instruct_label_text.set('Roll dice')
        self.instruct_label = tkinter.Label(self.dice_roll_box, textvariable = self.instruct_label_text, background = Phase.BG_COLOR, padx = 10, pady = 10, font = ('Arial', 16, 'bold'))
        self.instruct_label.place(in_ = self.dice_roll_box, relx = 0.05, rely = 0.75)
        self.instruct_label.bind('<Motion>', lambda evt: self.root.configure(cursor = Phase.CURSOR_HAND))
        self.instruct_label.bind('<Leave>', lambda evt: self.root.configure(cursor = Phase.CURSOR_DEFAULT))
        self.instruct_label.bind('<Button-1>', self.roll_dice)

        self.phase.deactivate_button()
        
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
        self.action_frame = self.action_tree_handler.create_action_frame(self.frame)
        self.action_cost_frame = self.action_tree_handler.create_action_cost_frame(self.frame)
        self.highlight_or_unhighlight_cards()
    
    def roll_dice(self, event):
        self.dice_rolled += 1
        if self.dice_rolled > 2:
            return
        self.phase.chaperone.roll_dice()
    
    def highlight_or_unhighlight_cards(self):
        for card_frames in self.card_frames.values():
            for card_frame in card_frames.values():
                card_frame.highlight_or_unhighlight_labels()
    
    def show_action_frame(self):
        self.action_frame.grid(row = 3, column = 0, sticky = 'ew')
        self.action_cost_frame.grid(row = 4, column = 0, sticky = 'ew')
        self.action_tree_handler.bind_events()
        self.phase.activate_button()

    def hide_action_frame(self):
        self.action_frame.grid_forget()
        self.action_cost_frame.grid_forget()
        self.phase.deactivate_button()

    def create_cards_frame(self, where, type, iterable):
        self.root.update_idletasks()
        frame_width = where.master.master.winfo_width() ### Get width of inner frame middle right
        outer_frame = tkinter.Frame(where, background = Phase.BG_COLOR, padx = 5, pady = 5)
        outer_frame_top = tkinter.Label(outer_frame, text = f'{type.title()} cards', anchor = tkinter.W, background = Phase.DARKER_BG_COLOR, font = ('Arial', 10, 'bold'))
        outer_frame_bottom = tkinter.Frame(outer_frame, background = Phase.DARKER_BG_COLOR, pady = 5)
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
            num_of_thing = self.phase.chaperone.player.num_of_card_type_in_hand(tup.name)
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
        top_label = tkinter.Label(outer_frame, text = 'Tokens remaining', background = Phase.DARKER_BG_COLOR, anchor = tkinter.W, font = ('Arial', 10, 'bold'))
        top_label.pack(fill = 'x', side = tkinter.TOP)
        bottom_frame = tkinter.Frame(outer_frame, background = Phase.DARKER_BG_COLOR)
        bottom_frame.pack(fill = 'x', side = tkinter.TOP)
        self.movable_piece_label_texts = {}
        for i, movable_piece in enumerate(['road', 'settlement', 'city', 'game']): ### Only add tokens if two players
            piece_label = tkinter.Label(bottom_frame, text = f'{movable_piece.title().replace("_", " ")}:', background = Phase.DARKER_BG_COLOR)
            piece_label.grid(row = 0, column = i * 2)
            num_label_text = tkinter.StringVar()
            num_label_text.set(str(self.player.num_tokens_available(movable_piece)))
            self.movable_piece_label_texts[movable_piece] = num_label_text
            num_label = tkinter.Label(bottom_frame, textvariable = num_label_text, background = Phase.DARKER_BG_COLOR)
            num_label.grid(row = 0, column = i * 2 + 1)
        return outer_frame
    
    def update_resource_cards(self):
        d = dict(Counter([resource_card.type for resource_card in self.phase.chaperone.player.hand['resource']]))
        for resource_type, num_label in self.card_num_label_texts['resource'].items():
            num_of_resource = d.get(resource_type, 0)
            num_label.set(str(num_of_resource))
        self.highlight_or_unhighlight_cards()
    
    def update_development_cards(self):
        d = dict(Counter([development_card.type for development_card in self.phase.chaperone.player.hand['development']]))
        for development_card_type, num_label in self.card_num_label_texts['development'].items():
            num_of_card = d.get(development_card_type, 0)
            num_label.set(str(num_of_card))
        self.highlight_or_unhighlight_cards()
    
    def update_movable_pieces(self):
        for movable_piece, num_label_text in self.movable_piece_label_texts.items():
            num_label_text.set(str(self.player.num_tokens_available(movable_piece)))