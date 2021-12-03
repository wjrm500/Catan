from actions.Action import Action

class EndTurn(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        self.data = data
        game_phase = chaperone.current_phase
        game_phase.update_active_player_index()
        game_phase.button['state'] = 'disable' ### Disable for all players even active client as dice roll happens first
        game_phase.button.configure({'background': '#cccccc'})
        game_phase.button_text.set('Disabled')
        frame_handler = game_phase.frame_handler_by_name(game_phase.notebook, 'play')
        if game_phase.client_active():
            frame_handler.start_turn()
            game_phase.instruction_text.set("It's your turn!")
            game_phase.instruction.configure({'background': '#90EE90'}) ### LightGreen
        elif chaperone.player.id == data['player'].id:
            frame_handler.end_turn()
            game_phase.instruction_text.set("Please wait for your turn")
            game_phase.instruction.configure({'background': '#F08080'}) ### LightCoral
        self.game_phase = game_phase
        text_area = self.get_text_area(in_settling_phase = False)
        self.enable_text_area(text_area)
        text_area.insert('end', f'\n\n{self.data["player"].name} ended their turn.', 'red_font')
        self.disable_text_area(text_area)