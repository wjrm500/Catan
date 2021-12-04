from actions.Action import Action

class TradeWithBank(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        self.chaperone = chaperone
        self.game_phase = self.chaperone.current_phase
        self.data = data
        self.reload_active_player()
        self.update_gui()
    
    def update_gui(self):
        is_instigating_client = self.data['player'].id == self.chaperone.player.id
        if is_instigating_client:
            self.refresh_play_frame_handler()