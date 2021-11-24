from actions.Action import Action

class RollDice(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        self.chaperone = chaperone
        self.game_phase = self.chaperone.current_phase
        self.data = data
        self.update_gui()
    
    def update_gui(self):
        dice_face_chars = {1: '\u2680', 2: '\u2681', 3: '\u2682', 4: '\u2683', 5: '\u2684', 6: '\u2685'}
        DiceRoll = self.data['dice_roll']
        is_instigating_client = self.data['player'].id == self.chaperone.player.id
        if is_instigating_client:
            display_text = f'{dice_face_chars[DiceRoll.roll_1]} + {dice_face_chars[DiceRoll.roll_2]} = {DiceRoll.total}'
            play_frame_handler = self.game_phase.notebook_frame_handlers['play']
            play_frame_handler.dice_roll_text.set(display_text)
            play_frame_handler.dice_roll_event_text.set(DiceRoll.event_text)