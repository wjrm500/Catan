from actions.Action import Action

class SwapCards(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        self.chaperone = chaperone
        self.game_phase = self.chaperone.current_phase
        self.data = data
        self.reload_all_players()
        self.update_gui()
    
    def update_gui(self):
        self.refresh_play_frame_handler()
        text_area = self.get_text_area(in_settling_phase = False)
        give_text = ' and '.join([f'{num} {resource_type}' for resource_type, num in self.data['give_resource_card_dict'].items()])
        receive_text = ' and '.join([f'{num} {resource_type}' for resource_type, num in self.data['receive_resource_card_dict'].items()])
        text = f'\n\n{self.data["player"].name} forced {self.data["random_opponent"].name} to swap their {receive_text} for {give_text}!'
        self.history_insert(text_area, text)