from actions.Action import Action

class RollDice(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        self.chaperone = chaperone
        self.game_phase = self.chaperone.current_phase
        self.data = data

        ### Update players client side (any player's hand might have changed)
        for player in data['players']:
            if self.chaperone.player.id == player.id:
                self.chaperone.player.__dict__ = player.__dict__

        self.update_gui()
    
    def update_gui(self):
        dice_face_chars = {1: '\u2680', 2: '\u2681', 3: '\u2682', 4: '\u2683', 5: '\u2684', 6: '\u2685'}
        DiceRoll = self.data['dice_roll']
        is_instigating_client = self.data['player'].id == self.chaperone.player.id
        play_frame_handler = self.game_phase.notebook_frame_handlers['play']
        if is_instigating_client:
            display_text = f'{dice_face_chars[DiceRoll.roll_1]} + {dice_face_chars[DiceRoll.roll_2]} = {DiceRoll.total}'
            play_frame_handler.dice_roll_text.set(display_text)
            event_text = '\n'.join(DiceRoll.text_events)
            play_frame_handler.dice_roll_event_text.set(event_text)
            if DiceRoll.proceed_to_action_selection:
                play_frame_handler.instruct_label_text.set('Take actions')
                play_frame_handler.instruct_label.bind('<Button-1>', play_frame_handler.transition_to_action_selection)
            else:
                play_frame_handler.instruct_label_text.set('Roll dice again')
        else:
            play_frame_handler.update_resource_cards()
            play_frame_handler.action_tree_handler.fill_action_tree()
        text_area = self.get_text_area(in_settling_phase = False)
        self.enable_text_area(text_area)
        event_text = ' '.join(DiceRoll.text_events)
        text_area.insert('end', f'\n\n{self.data["player"].name} rolled a {DiceRoll.total}. {event_text}')
        self.disable_text_area(text_area)