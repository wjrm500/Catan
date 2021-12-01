import tkinter
from tkinter import ttk

from frontend.Tkinter.phases.game.GamePhase import GamePhase
from frontend.Tkinter.phases.game.sub_phases.notebook_frame_handlers.ChatFrameHandler import ChatFrameHandler
from frontend.Tkinter.phases.game.sub_phases.notebook_frame_handlers.HistoryFrameHandler import HistoryFrameHandler
from frontend.Tkinter.phases.game.sub_phases.notebook_frame_handlers.PlayFrameHandler import PlayFrameHandler
from frontend.Tkinter.phases.game.sub_phases.notebook_frame_handlers.StatusFrameHandler import StatusFrameHandler
from frontend.Tkinter.rendering.HexagonRendering import HexagonRendering

class MainGamePhase(GamePhase):
    def update_active_player_index(self):
        self.active_player_index += 1
        if self.active_player_index > len(self.chaperone.players) - 1:
            self.active_player_index = 0
    
    def setup_inner_frame_top_right(self):
        super().setup_inner_frame_top_right('MAIN GAME PHASE')
    
    def setup_inner_frame_middle_left(self):
        canvas_mode = HexagonRendering.CANVAS_MODE_DEFAULT
        return super().setup_inner_frame_middle_left(canvas_mode)
    
    def setup_inner_frame_middle_right(self):
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
            if not hasattr(self, 'play_frame_handler'):
                self.play_frame_handler = PlayFrameHandler(self, notebook)
            frame_handler = self.play_frame_handler
        elif frame_name == 'status':
            if not hasattr(self, 'status_frame_handler'):
                self.status_frame_handler = StatusFrameHandler(self, notebook)
            frame_handler = self.status_frame_handler
        elif frame_name == 'history':
            if not hasattr(self, 'history_frame_handler'):
                self.history_frame_handler = HistoryFrameHandler(self, notebook)
            frame_handler = self.history_frame_handler
        elif frame_name == 'chat':
            if not hasattr(self, 'chat_frame_handler'):
                self.chat_frame_handler = ChatFrameHandler(self, notebook)
            frame_handler = self.chat_frame_handler
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
        self.root.bind('<Configure>', self.resize_card_labels, '+')
        self.root.bind('<Configure>', lambda evt: self.notebook.config(height = self.inner_frame_middle_right.winfo_height()))
        super().run()
    
    def resize_card_labels(self, event):
        play_frame_handler = self.notebook_frame_handlers['play']
        frame_width = play_frame_handler.get().winfo_width()
        for label in play_frame_handler.labels:
            label.configure({'width': round(frame_width / 50), 'wraplength': round(frame_width / 8)})
    
    def activate_button(self):
        self.button_text.set('End turn')
        self.button['state'] = 'normal'
        self.button.configure({'background': '#90EE90'}) ### LightGreen
        self.button.bind('<Motion>', lambda evt: self.root.configure(cursor = self.CURSOR_HAND))
        self.button.bind('<Leave>', lambda evt: self.root.configure(cursor = self.CURSOR_DEFAULT))
        self.button.bind('<Button-1>', self.end_turn)
    
    def deactivate_button(self):
        self.button_text.set('Disabled')
        self.button['state'] = 'disable'
        self.button.configure({'background': '#cccccc'}) ### LightGreen
        self.button.unbind('<Motion>')
        self.button.unbind('<Leave>')
        self.button.unbind('<Button-1>')
    
    def end_turn(self, event):
        self.root.configure(cursor = self.CURSOR_DEFAULT)
        self.chaperone.end_turn()