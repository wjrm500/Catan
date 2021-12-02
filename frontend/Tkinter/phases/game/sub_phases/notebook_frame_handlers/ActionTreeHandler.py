import tkinter
from tkinter import ttk

from config import config
from frontend.ColorUtils import ColorUtils
from frontend.Tkinter.phases.Phase import Phase
from frontend.Tkinter.rendering.HexagonRendering import HexagonRendering

class ActionTreeHandler:
    def __init__(self, play_frame_handler):
        self.play_frame_handler = play_frame_handler

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
            enabled_tag = 'enabled' if self.play_frame_handler.player.can_afford(action_const) else 'disabled'
            self.action_tree.insert('', tkinter.END, iid = action_const, text = action_const, values = (action_data['name'],), tags = (even_tag, enabled_tag))
    
    def action_tree_motion_handler(self, event):
        item = self.action_tree.identify('item', event.x, event.y)
        item = self.action_tree.item(item)
        action, tags = item['text'], item['tags']
        self.play_frame_handler.root.configure({'cursor': Phase.CURSOR_HAND if 'enabled' in tags else Phase.CURSOR_DEFAULT})
        self.show_action_cost(action)
    
    def action_tree_click_handler(self, event):
        item = self.action_tree.identify('item', event.x, event.y)
        item = self.action_tree.item(item)
        action, tags = item['text'], item['tags']
        if 'enabled' in tags:
            self.fire_method_from_action(action)
    
    def action_tree_leave_handler(self, event):
        self.play_frame_handler.root.configure({'cursor': Phase.CURSOR_DEFAULT})
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
    
    def bind_events(self):
        self.action_tree.bind('<Motion>', self.action_tree_motion_handler)
        self.action_tree.bind('<Button-1>', self.action_tree_click_handler)
        self.action_tree.bind('<Leave>', self.action_tree_leave_handler)
    
    def fire_method_from_action(self, action):
        if action == 'BUILD_ROAD':
            self.handle_build_road()
        elif action == 'BUILD_SETTLEMENT':
            self.handle_build_settlement()
    
    def handle_build_road(self):
        phase = self.play_frame_handler.phase
        hexagon_rendering = phase.hexagon_rendering
        hexagon_rendering.canvas_mode = HexagonRendering.CANVAS_MODE_BUILD_ROAD

        phase.instruction_text.set('Build a road!')
        instruction_bg_color = '#9400D3' ### DarkViolet
        phase.instruction.configure({'background': instruction_bg_color, 'foreground': ColorUtils.get_fg_from_bg(instruction_bg_color)})

        ### Bottom right corner button
        phase.button_text.set('Cancel')
        button_bg_color = '#FF0000' ### Red
        phase.button.configure({'background': button_bg_color, 'foreground': ColorUtils.get_fg_from_bg(button_bg_color)})
        phase.button.bind('<Button-1>', self.cancel)
    
    def handle_build_settlement(self):
        phase = self.play_frame_handler.phase
        hexagon_rendering = phase.hexagon_rendering
        hexagon_rendering.canvas_mode = HexagonRendering.CANVAS_MODE_BUILD_SETTLEMENT

        phase.instruction_text.set('Build a settlement!')
        instruction_bg_color = '#9400D3' ### DarkViolet
        phase.instruction.configure({'background': instruction_bg_color, 'foreground': ColorUtils.get_fg_from_bg(instruction_bg_color)})

        ### Bottom right corner button
        phase.button_text.set('Cancel')
        button_bg_color = '#FF0000' ### Red
        phase.button.configure({'background': button_bg_color, 'foreground': ColorUtils.get_fg_from_bg(button_bg_color)})
        phase.button.bind('<Button-1>', self.cancel)
    
    def cancel(self, event):
        phase = self.play_frame_handler.phase
        hexagon_rendering = phase.hexagon_rendering
        hexagon_rendering.canvas_mode = HexagonRendering.CANVAS_MODE_DEFAULT

        phase.instruction_text.set("It's your turn!")
        instruction_bg_color = '#90EE90' ### LightGreen
        phase.instruction.configure({'background': instruction_bg_color, 'foreground': ColorUtils.get_fg_from_bg(instruction_bg_color)})

        ### Bottom right corner button
        phase.button_text.set('End turn')
        button_bg_color = '#90EE90' ### LightGreen
        phase.button.configure({'background': button_bg_color, 'foreground': ColorUtils.get_fg_from_bg(button_bg_color)})
        phase.button.bind('<Button-1>', phase.end_turn)