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
        if action == 'BUILD_ROAD':
            self.handle_build_road()
        elif action == 'BUILD_SETTLEMENT':
            self.handle_build_settlement()
        elif action == 'TRADE_WITH_BANK':
            self.handle_trade_with_bank()
    
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
        
    def handle_trade_with_bank(self):
        self.trade_with_bank_setup()
        self.set_instruction('Trade with the bank!')
        self.set_cancel_button()
    
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
            self.trade_with_bank_overlay.destroy()

    def trade_with_bank_setup(self):
        self.play_frame_handler.root.update_idletasks()
        frame_width = self.frame.master.master.winfo_width() ### Get width of inner frame middle right
        self.trade_with_bank_overlay = tkinter.Frame(self.frame, background = Phase.BG_COLOR)
        self.trade_with_bank_overlay.grid_columnconfigure(0, weight = 1)
        self.trade_with_bank_overlay.place(in_ = self.frame, anchor = tkinter.CENTER, relheight = 1, relwidth = 1, relx = 0.5, rely = 0.5)
        darker_blue = ColorUtils.darken_hex(Phase.BG_COLOR, 0.2)
    
        player = self.play_frame_handler.player
        hand_dict = dict(Counter([resource_card.type for resource_card in self.phase.chaperone.player.hand['resource']]))
        port_types = player.port_types()
        Card = namedtuple('Card', ['resource_type', 'cost'])
        give_iterable = [Card(resource_type, cost) for resource_type, num in hand_dict.items() if num >= (cost := player.bank_trade_cost(port_types, resource_type))]
        receive_iterable = [Card(resource_type, 1) for resource_type in config['resource_types'].keys() if resource_type != 'desert']
        give_iterable = {
            'title': 'What do you want to give?',
            'iterable': give_iterable
        }
        receive_iterable = {
            'title': 'What do you want to receive?',
            'iterable': receive_iterable
        }
        for i, iterable in enumerate([give_iterable, receive_iterable]):
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
                inner_frame.grid(row = 0, column = j, padx = 2.5)
            outer_frame.grid(row = i, column = 0, sticky = 'ew')