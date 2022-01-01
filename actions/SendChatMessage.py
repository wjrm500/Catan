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

    def update_gui(self):
        text_area = self.get_chat_text_area()
        text = f'\n\n{self.data["player"].name}: {self.data["message"]}'
        self.text_insert(text_area, text, 'purple_font')