from actions.Action import Action

class PlayMonopolyCard(Action):
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
        self.refresh_play_frame_handler()
        text_area = self.get_history_text_area(in_settling_phase = False)
        text = f'\n\n{self.data["player"].name} played a Monopoly card and asked for everybody\'s {self.data["resource_type"]}... and received {self.data["num_received"]}!'
        self.text_insert(text_area, text, 'purple_font')
        if self.is_instigating_client() and self.data['num_received'] == 0:
            history_frame_handler = self.game_phase.notebook_frame_handlers['history']
            self.game_phase.notebook.select(history_frame_handler.get())