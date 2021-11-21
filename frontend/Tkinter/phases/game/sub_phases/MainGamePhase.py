import tkinter
from tkinter import ttk
from frontend.ColorUtils import ColorUtils
from frontend.Tkinter.phases.game.GamePhase import GamePhase
from frontend.Tkinter.phases.game.sub_phases.notebook_frame_handlers.ChatFrameHandler import ChatFrameHandler
from frontend.Tkinter.phases.game.sub_phases.notebook_frame_handlers.HistoryFrameHandler import HistoryFrameHandler
from frontend.Tkinter.phases.game.sub_phases.notebook_frame_handlers.PlayFrameHandler import PlayFrameHandler
from frontend.Tkinter.phases.game.sub_phases.notebook_frame_handlers.StatusFrameHandler import StatusFrameHandler

class MainGamePhase(GamePhase):
    def update_active_player_index(self):
        self.active_player_index += 1
        if self.active_player_index > len(self.players) - 1:
            self.active_player_index = 0
    
    def setup_inner_frame_top_right(self):
        super().setup_inner_frame_top_right('MAIN GAME PHASE')
    
    def setup_inner_frame_middle_right(self):
        style = ttk.Style()
        darker_blue = ColorUtils.darken_hex(self.BG_COLOR, 0.2)
        style.theme_create('catan', parent = 'classic', settings = {
            'TNotebook': {
                'configure': {'background': self.BG_COLOR, 'tabmargins': [0, 0]}
            },
            'TNotebook.Tab': {
                'configure': {'background': self.BG_COLOR, 'padding': [5, 5]},
                'map': {'background': [('selected', darker_blue)]}
            }
        })
        style.theme_use('catan')
        self.notebook = ttk.Notebook(self.inner_frame_middle_right)
        self.notebook_frame_handlers = {}
        for frame_name in ['play', 'status', 'history', 'chat']:
            frame_handler = self.frame_handler_by_name(self.notebook, frame_name)
            frame_handler.setup()
            frame = frame_handler.get()
            frame.pack(expand = True, fill = 'both')
            self.notebook.add(frame, text = frame_name.title())
            self.notebook_frame_handlers[frame_name] = frame_handler
        self.notebook.pack(fill = 'both', padx = 10, pady = 10)
    
    def frame_handler_by_name(self, notebook, frame_name):
        if frame_name == 'play':
            frame_handler = PlayFrameHandler(self.root, notebook)
        elif frame_name == 'status':
            frame_handler = StatusFrameHandler(self.root, notebook)
        elif frame_name == 'history':
            frame_handler = HistoryFrameHandler(self.root, notebook)
        elif frame_name == 'chat':
            frame_handler = ChatFrameHandler(self.root, notebook)
        return frame_handler

    def play_frame(self):
        frame = tkinter.Frame(self.notebook)
        return frame
    
    def status_frame(self):
        frame = tkinter.Frame(self.notebook)
        return frame

    def history_frame(self):
        frame = tkinter.Frame(self.notebook)
        return frame

    def chat_frame(self):
        frame = tkinter.Frame(self.notebook)
        return frame
    
    def setup_inner_frame_bottom_left(self):
        client_active = self.client_active()
        instruction_text = "It's your turn!" if client_active else 'Please wait for your turn'
        label_bg_color = '#90EE90' if client_active else '#F08080' ### LightGreen or LightCoral
        return super().setup_inner_frame_bottom_left(instruction_text, label_bg_color)
    
    def run(self):
        self.root.bind('<Configure>', self.resize_, '+')
        super().run()
    
    def resize_(self, event):
        play_frame = self.notebook_frame_handlers['play']
        frame_width = play_frame.get().winfo_width()
        for label in play_frame.labels:
            label.configure({'width': round(frame_width / 50), 'wraplength': round(frame_width / 8)})