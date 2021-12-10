from collections import Counter, namedtuple
from functools import partial
import tkinter
from tkinter import ttk

from config import config
from frontend.ColorUtils import ColorUtils
from frontend.Tkinter.phases.Phase import Phase
from frontend.Tkinter.phases.game.sub_phases.notebook_frame_handlers.CardFrame import CardFrame
from frontend.Tkinter.phases.game.sub_phases.notebook_frame_handlers.CardFrameLabel import CardFrameLabel
from frontend.Tkinter.rendering.HexagonRendering import HexagonRendering

class ActionTreeHandler:
    def __init__(self, play_frame_handler):
        self.play_frame_handler = play_frame_handler
        self.frame = self.play_frame_handler.frame
        self.phase = self.play_frame_handler.phase
        self.hexagon_rendering = self.phase.hexagon_rendering
        self.development_card_clicked = False

    def create_action_frame(self, where):
        outer_frame = tkinter.Frame(where, background = Phase.BG_COLOR, padx = 5, pady = 5)
        darker_blue = ColorUtils.darken_hex(Phase.BG_COLOR, 0.2)
        inner_frame = tkinter.Frame(outer_frame, background = darker_blue, padx = 5, pady = 5)
        inner_frame.pack(side = tkinter.TOP, expand = True, fill = 'both')
        self.action_tree = ttk.Treeview(inner_frame, columns = ['action'], show = 'headings', height = 5)
        self.action_tree.tag_configure('odd', background = Phase.BG_COLOR)
        self.action_tree.tag_configure('even', background = ColorUtils.darken_hex(Phase.BG_COLOR, 0.05))
        self.action_tree.tag_configure('disabled', foreground = '#808080')
        self.action_tree.tag_configure('enabled', foreground = 'black')
        self.action_tree.tag_configure('clicked', background = '#9400D3', foreground = '#FFFFFF') ### DarkViolet | White
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
            enabled_tag = 'enabled' if self.play_frame_handler.player.can_do(action_const) else 'disabled'
            self.action_tree.insert('', tkinter.END, iid = action_const, text = action_const, values = (action_data['name'],), tags = (even_tag, enabled_tag))
    
    def action_tree_motion_handler(self, event):
        item = self.action_tree.identify('item', event.x, event.y)
        item = self.action_tree.item(item)
        action, tags = item['text'], item['tags']
        self.play_frame_handler.root.configure({'cursor': Phase.CURSOR_HAND if 'enabled' in tags else Phase.CURSOR_DEFAULT})
        self.show_action_cost(action)
    
    def action_tree_click_handler(self, event):
        ### If another action already clicked, reset
        for iid in self.action_tree.tag_has('clicked'):
            even_tag = self.clicked_treeview_item_even_tag
            self.action_tree.item(iid, tags = (even_tag, 'enabled'))

        item = self.action_tree.identify('item', event.x, event.y)
        item = self.action_tree.item(item)
        action, tags = item['text'], item['tags']
        if 'enabled' in tags:
            self.fire_method_from_action(action)
            self.action_tree.item(action, tags = ('clicked'))
            self.clicked_treeview_item_even_tag = 'even' if 'even' in tags else 'odd'
    
    def action_tree_leave_handler(self, event):
        self.play_frame_handler.root.configure({'cursor': Phase.CURSOR_DEFAULT})
        self.action_cost.set(self.default_action_cost_text())
    
    def show_action_cost(self, action):
        if action:
            if (cost := config['actions'][action].get('cost')):
                cost_texts = []
                if (resources := cost.get('resources')):
                    resources_text = f'Resources: {", ".join(resources)}'
                    cost_texts.append(resources_text)
                if (other := cost.get('other')):
                    other_text = f'Other: {", ".join(other)}'
                    cost_texts.append(other_text)
                cost_text = ' | '.join(cost_texts)                                                  
            else:
                ### Calculate cost dynamically
                cost_text = ''
        else:
            cost_text = self.default_action_cost_text()
        self.action_cost.set(cost_text)
    
    def default_action_cost_text(self):
        return 'Hover over an action to see how much it costs!'
    
    def bind_events(self):
        self.action_tree.bind('<Motion>', self.action_tree_motion_handler)
        self.action_tree.bind('<Button-1>', self.action_tree_click_handler)
        self.action_tree.bind('<Leave>', self.action_tree_leave_handler)
    
    def fire_method_from_action(self, action):
        ### Consts from ActionFactory not used due to circular import error
        if action == 'BUILD_ROAD':
            self.handle_build_road()
        elif action == 'BUILD_SETTLEMENT':
            self.handle_build_settlement()
        elif action == 'BUY_DEVELOPMENT_CARD':
            self.handle_buy_development_card()
        elif action == 'TRADE_WITH_BANK':
            self.handle_trade_with_bank()
        elif action == 'USE_DEVELOPMENT_CARD':
            self.handle_use_development_card()
    
    def set_cancel_button(self):
        self.phase.button_text.set('Cancel')
        button_bg_color = '#FF0000' ### Red
        self.phase.button.configure({'background': button_bg_color, 'foreground': ColorUtils.get_fg_from_bg(button_bg_color)})
        self.phase.button.bind('<Button-1>', self.cancel)
    
    def set_instruction(self, instruction_text):
        self.phase.instruction_text.set(instruction_text)
        instruction_bg_color = '#9400D3' ### DarkViolet
        self.phase.instruction.configure({'background': instruction_bg_color, 'foreground': ColorUtils.get_fg_from_bg(instruction_bg_color)})
    
    def handle_build_road(self):
        self.hexagon_rendering.canvas_mode = HexagonRendering.CANVAS_MODE_BUILD_ROAD
        self.set_instruction('Build a road!')
        self.set_cancel_button()
    
    def handle_build_settlement(self):
        self.hexagon_rendering.canvas_mode = HexagonRendering.CANVAS_MODE_BUILD_SETTLEMENT
        self.set_instruction('Build a settlement!')
        self.set_cancel_button()
    
    def handle_buy_development_card(self):
        self.phase.chaperone.buy_development_card()
    
    def handle_trade_with_bank(self):
        self.trade_with_bank_setup()
        self.set_instruction('Trade with the bank!')
        self.set_cancel_button()
    
    def handle_use_development_card(self):
        for type, card_frame in self.play_frame_handler.card_frames['development'].items():
            func = self.get_development_card_func_from_type(type)
            card_frame.make_labels_clickable_or_unclickable(event_handler = func)
        self.set_instruction('Select a development card!')
        self.set_cancel_button()
    
    def get_development_card_func_from_type(self, type):
        if type == 'knight':
            return self.knight_card_click
        elif type == 'monopoly':
            return self.monopoly_card_click
        elif type == 'road_building':
            return self.road_building_card_click
        elif type == 'year_of_plenty':
            return self.year_of_plenty_card_click
    
    def knight_card_click(self, event):
        self.development_card_clicked = True
        self.hexagon_rendering.canvas_mode = HexagonRendering.CANVAS_MODE_PLACE_ROBBER
        self.set_instruction('Place the robber!')
    
    def monopoly_card_click(self, event):
        self.development_card_clicked = True
        self.hexagon_rendering.canvas_mode = HexagonRendering.CANVAS_MODE_DISABLED
        self.set_instruction('Select a resource card!')
        for card_frame in self.play_frame_handler.card_frames['resource'].values():
            func = lambda evt, card_frame = card_frame: self.phase.chaperone.play_monopoly_card(card_frame.get_type()) ### Using default argument for closure https://stackoverflow.com/questions/7546285/creating-lambda-inside-a-loop
            card_frame.make_labels_clickable(event_handler = func)

    def road_building_card_click(self, event):
        self.development_card_clicked = True
        self.road_building_turn_index = 0
        self.hexagon_rendering.canvas_mode = HexagonRendering.CANVAS_MODE_BUILD_ROAD
        self.set_instruction('Build a road!')

    def year_of_plenty_card_click(self, event):
        self.development_card_clicked = True
        self.hexagon_rendering.canvas_mode = HexagonRendering.CANVAS_MODE_DISABLED
    
    def cancel(self, event):
        phase = self.play_frame_handler.phase
        hexagon_rendering = phase.hexagon_rendering
        hexagon_rendering.canvas_mode = HexagonRendering.CANVAS_MODE_DEFAULT
        phase.instruction_text.set("It's your turn!")
        instruction_bg_color = '#90EE90' ### LightGreen
        phase.instruction.configure({'background': instruction_bg_color, 'foreground': ColorUtils.get_fg_from_bg(instruction_bg_color)})
        phase.button_text.set('End turn')
        button_bg_color = '#90EE90' ### LightGreen
        phase.button.configure({'background': button_bg_color, 'foreground': ColorUtils.get_fg_from_bg(button_bg_color)})
        phase.button.bind('<Button-1>', phase.end_turn)
        for iid in self.action_tree.tag_has('clicked'):
            even_tag = self.clicked_treeview_item_even_tag
            self.action_tree.item(iid, tags = (even_tag, 'enabled'))
        if hasattr(self, 'trade_with_bank_overlay'):
            for verb in ['give', 'receive']:
                for card_frame in self.trade_with_bank_card_frames[verb]:
                    card_frame.unhighlight_labels()
            self.trade_with_bank_summary_text.set('')
            self.trade_with_bank_confirm_button.configure({'background': '#DCDCDC', 'foreground': '#808080'})
            self.trade_with_bank_confirm_button.unbind('<Button-1>')
            self.trade_with_bank_confirm_button.unbind('<Motion>')
            self.trade_with_bank_confirm_button.unbind('<Leave>')
            self.trade_with_bank_overlay.place_forget()
        for card_frame in self.play_frame_handler.card_frames['development'].values():
            card_frame.make_labels_unclickable()
        if self.development_card_clicked:
            self.play_frame_handler.update_resource_cards()
            self.play_frame_handler.update_development_cards()
            self.play_frame_handler.update_movable_pieces()
            self.fill_action_tree()
        self.development_card_clicked = False

    def trade_with_bank_setup(self):
        darker_blue = ColorUtils.darken_hex(Phase.BG_COLOR, 0.2)
        Card = namedtuple('Card', ['resource_type', 'cost'])
        def handle_iterable(enumerator, iterable):
            self.trade_with_bank_card_frames[iterable['name']] = []
            outer_frame = tkinter.Frame(self.trade_with_bank_overlay, background = Phase.BG_COLOR, padx = 5, pady = 5)
            outer_frame_top = tkinter.Label(outer_frame, text = iterable['title'], anchor = tkinter.W, background = darker_blue, font = ('Arial', 10, 'bold'))
            outer_frame_bottom = tkinter.Frame(outer_frame, background = darker_blue, pady = 5)
            outer_frame_top.pack(fill = 'x', side = tkinter.TOP)
            outer_frame_bottom.pack(fill = 'x', side = tkinter.TOP)
            outer_frame.grid_rowconfigure(0, weight = 1)
            for j, tup in enumerate(iterable['iterable']):
                outer_frame_bottom.grid_columnconfigure(j, weight = 1, uniform = 'catan')
                inner_frame = CardFrame(outer_frame_bottom, highlightbackground = '#808080', highlightthickness = 3)
                bg_color = config['resource_types'][tup.resource_type]['color']
                label_partial = partial(CardFrameLabel, master = inner_frame, background = bg_color, width = round(frame_width / 50), wraplength = round(frame_width / 8))
                type_label = label_partial(height = 1, text = tup.resource_type.title())
                num_label = label_partial(font = ('Arial', '12', 'bold'), height = 1, text = tup.cost)
                type_label.pack(expand = True, fill = 'both', side = tkinter.TOP)
                num_label.pack(expand = True, fill = 'both', side = tkinter.TOP)
                for label in [type_label, num_label]:
                    label.event_handler = iterable['card_click_event_handler']
                inner_frame.grid(row = 0, column = j, padx = 2.5)
                self.trade_with_bank_card_frames[iterable['name']].append(inner_frame)
            outer_frame.grid(row = enumerator, column = 0, sticky = 'ew')
        self.give_type = ''
        self.receive_type = ''
        self.play_frame_handler.root.update_idletasks()
        frame_width = self.frame.master.master.winfo_width() ### Get width of inner frame middle right
        if not hasattr(self, 'trade_with_bank_overlay'):
            self.trade_with_bank_overlay = tkinter.Frame(self.frame, background = Phase.BG_COLOR)
            self.trade_with_bank_overlay.grid_columnconfigure(0, weight = 1)

            ### "What do you want to receive?" section
            receive_iterable = [Card(resource_type, 1) for resource_type in config['resource_types'].keys() if resource_type != 'desert']
            receive_iterable = {
                'name': 'receive',
                'title': 'What do you want to receive?',
                'card_click_event_handler': self.receive_card_click,
                'iterable': receive_iterable
            }
            self.trade_with_bank_card_frames = {}
            handle_iterable(1, receive_iterable)
        
            ### Summary section
            outer_frame = tkinter.Frame(self.trade_with_bank_overlay, background = Phase.BG_COLOR, padx = 5, pady = 5)
            outer_frame_top = tkinter.Label(outer_frame, text = 'Summary', anchor = tkinter.W, background = darker_blue, font = ('Arial', 10, 'bold'))
            self.trade_with_bank_summary_text = tkinter.StringVar()
            self.trade_with_bank_summary_text.set('')
            outer_frame_bottom = tkinter.Label(outer_frame, textvariable = self.trade_with_bank_summary_text, background = darker_blue, anchor = tkinter.W, font = ('Arial', 10))
            outer_frame_top.pack(fill = 'x', side = tkinter.TOP)
            outer_frame_bottom.pack(fill = 'x', side = tkinter.TOP)
            outer_frame.grid(row = 2, column = 0, sticky = 'ew')

            ### Confirm button
            outer_frame = tkinter.Frame(self.trade_with_bank_overlay, background = Phase.BG_COLOR, padx = 5, pady = 5)
            self.trade_with_bank_confirm_button = tkinter.Button(outer_frame, text = 'Confirm', background = '#DCDCDC', foreground = '#808080', anchor = tkinter.W) ### Disabled before activated
            self.trade_with_bank_confirm_button.pack(side = tkinter.TOP)
            outer_frame.grid(row = 3, column = 0, sticky = 'ew')

        ### "What do you want to give?" section
        player = self.play_frame_handler.player
        hand_dict = dict(Counter([resource_card.type for resource_card in self.phase.chaperone.player.hand['resource']]))
        port_types = player.port_types()
        give_iterable = [Card(resource_type, cost) for resource_type, num in hand_dict.items() if num >= (cost := player.bank_trade_cost(resource_type, port_types))]
        give_iterable = {
                'name': 'give',
                'title': 'What do you want to give?',
                'card_click_event_handler': self.give_card_click,
                'iterable': give_iterable
            }
        handle_iterable(0, give_iterable)

        ### Make clickable
        for verb in ['give', 'receive']:
            for card_frame in self.trade_with_bank_card_frames[verb]:
                for label in card_frame.winfo_children():
                    label.bind('<Button-1>', label.event_handler)
                    label.bind('<Motion>', lambda evt: self.play_frame_handler.root.configure(cursor = Phase.CURSOR_HAND))
                    label.bind('<Leave>', lambda evt: self.play_frame_handler.root.configure(cursor = Phase.CURSOR_DEFAULT))
        
        self.trade_with_bank_overlay.place(in_ = self.frame, anchor = tkinter.CENTER, relheight = 1, relwidth = 1, relx = 0.5, rely = 0.5)
    
    def give_card_click(self, event):
        for card_frame in self.trade_with_bank_card_frames['give']:
            card_frame.unhighlight_labels()
        card_frame = event.widget.master
        card_frame.highlight_labels()
        self.give_type = card_frame.get_type()
        self.update_trade_with_bank_summary_text()
        self.activate_confirm_button_if_give_and_receive()
    
    def receive_card_click(self, event):
        for card_frame in self.trade_with_bank_card_frames['receive']:
            card_frame.unhighlight_labels()
        card_frame = event.widget.master
        card_frame.highlight_labels()
        self.receive_type = card_frame.get_type()
        self.update_trade_with_bank_summary_text()
        self.activate_confirm_button_if_give_and_receive()
    
    def update_trade_with_bank_summary_text(self):
        summary_text_components = ['You will']
        give_and_receive_text_components = []
        if self.give_type != '':
            give_and_receive_text_components.append(f'give {self.give_type}')
        if self.receive_type != '':
            give_and_receive_text_components.append(f'receive {self.receive_type}')
        summary_text_components.append(' and '.join(give_and_receive_text_components))
        self.trade_with_bank_summary_text.set('{}.'.format(' '.join(summary_text_components)))
    
    def activate_confirm_button_if_give_and_receive(self):
        if self.give_type != '' and self.receive_type != '':
            self.trade_with_bank_confirm_button.configure({'background': '#90EE90', 'foreground': '#000000'}) ### LightGreen | Black
            self.trade_with_bank_confirm_button.bind('<Button-1>', self.trade_with_bank)
            self.trade_with_bank_confirm_button.bind('<Motion>', lambda evt: self.play_frame_handler.root.configure(cursor = Phase.CURSOR_HAND))
            self.trade_with_bank_confirm_button.bind('<Leave>', lambda evt: self.play_frame_handler.root.configure(cursor = Phase.CURSOR_DEFAULT))
    
    def trade_with_bank(self, event):
        self.phase.chaperone.trade_with_bank(self.give_type, self.receive_type)