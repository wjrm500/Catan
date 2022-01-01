from datetime import datetime
from actions.Action import Action

class SendChatMessage(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        self.chaperone = chaperone
        self.game_phase = self.chaperone.current_phase
        self.data = data
        self.hexagon_rendering = chaperone.current_phase.hexagon_rendering
        self.reload_all_players()
        self.update_gui()
        self.game_phase.notebook_frame_handlers['chat'].text_inserted = True

    def update_gui(self):
        text_area = self.get_chat_text_area()
        prefix = '\n' if self.game_phase.notebook_frame_handlers['chat'].text_inserted else ''
        self.text_insert(text_area, prefix)
        datetime_text = f'[{datetime.now().strftime("%H:%M:%S")}] '
        self.text_insert(text_area, datetime_text, 'datetime_font')
        name_text = self.data['player'].name
        self.text_insert(text_area, name_text, f'{self.data["player"].name}_font')
        message_text = f': {self.data["message"]}'
        self.text_insert(text_area, message_text)