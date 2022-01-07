from actions.Action import Action
from frontend.Tkinter.phases.Phase import Phase

class PlayYearOfPlentyCard(Action):
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
        text_area = self.get_history_text_area(in_settling_phase = False)
        if self.data['year_of_plenty_turn_index'] == 0:
            text = f'\n\n{self.data["player"].name} played a Year of Plenty card...'
            self.text_insert(text_area, text, 'purple_font')
        if self.data['bank_unable_to_pay']:
            text = f'\n\n{self.data["player"].name} requested {self.data["resource_type"]} from the bank... but the bank cannot afford to pay!'
            if self.is_instigating_client():
                history_frame_handler = self.game_phase.notebook_frame_handlers['history']
                self.game_phase.notebook.select(history_frame_handler.get())
        else:
            text = f'\n\n{self.data["player"].name} took 1 {self.data["resource_type"]} from the bank.'
            play_frame_handler = self.game_phase.notebook_frame_handlers['play']
            if self.is_instigating_client():
                if self.data['year_of_plenty_turn_index'] == 0:
                    self.game_phase.instruction_text.set('Select another resource!')
                    play_frame_handler.update_resource_cards()
                    play_frame_handler.action_tree_handler.year_of_plenty_turn_index += 1
                else:
                    play_frame_handler.root.configure(cursor = Phase.CURSOR_DEFAULT)
                    self.refresh_play_frame_handler()
        self.text_insert(text_area, text)