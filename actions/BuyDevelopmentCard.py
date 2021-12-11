from actions.Action import Action

class BuyDevelopmentCard(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        self.chaperone = chaperone
        self.game_phase = self.chaperone.current_phase
        self.data = data
        self.hexagon_rendering = chaperone.current_phase.hexagon_rendering
        self.reload_active_player()
        self.update_gui()

    def update_gui(self):
        text_area = self.get_text_area(in_settling_phase = False)
        text = f'\n\n{self.data["player"].name} bought a development card.'
        self.history_insert(text_area, text, 'purple_font')
        if self.is_instigating_client():
            self.refresh_play_frame_handler()