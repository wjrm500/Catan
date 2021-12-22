from actions.Action import Action
from frontend.ColorUtils import ColorUtils
from frontend.Tkinter.rendering.HexagonRendering import HexagonRendering

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
        play_frame_handler = self.game_phase.notebook_frame_handlers['play']
        if self.is_instigating_client():
            display_text = f'{dice_face_chars[DiceRoll.roll_1]} + {dice_face_chars[DiceRoll.roll_2]} = {DiceRoll.total}'
            play_frame_handler.dice_roll_text.set(display_text)
            
            if DiceRoll.proceed_to_action_selection:
                play_frame_handler.instruct_label_text.set('Take actions')
                play_frame_handler.instruct_label.bind('<Button-1>', play_frame_handler.transition_to_action_selection)
            else:
                play_frame_handler.instruct_label_text.set('Roll dice again')
            event_text = '\n'.join(DiceRoll.text_events)
            if DiceRoll.total == 7:
                event_text = 'Click on the hexagon you want to move the robber to!'
                self.prepare_for_robber_moving(play_frame_handler)
            play_frame_handler.dice_roll_event_text.set(event_text)
        else:
            play_frame_handler.update_resource_cards()
            play_frame_handler.action_tree_handler.fill_action_tree()
        text_area = self.get_text_area(in_settling_phase = False)
        event_text = ' '.join(DiceRoll.text_events)
        text = f'\n\n{self.data["player"].name} rolled a {DiceRoll.total}. {event_text}'
        self.history_insert(text_area, text)

        status_frame_handler = self.game_phase.notebook_frame_handlers['status']
        status_frame_handler.load_dice_roll_num_distro_frame()
        status_frame_handler.update_resources_won_table_frame()
        status_frame_handler.update_resources_lost_to_robber_table_frame()
    
    def prepare_for_robber_moving(self, play_frame_handler):
        self.game_phase.hexagon_rendering.canvas_mode = HexagonRendering.CANVAS_MODE_PLACE_ROBBER
        play_frame_handler.instruct_label.configure({'background': '#808080'})
        play_frame_handler.instruct_label.unbind('<Button-1>')
        play_frame_handler.instruct_label.unbind('<Motion>')
        play_frame_handler.instruct_label.unbind('<Leave>')
        self.game_phase.instruction_text.set('Place the robber!')
        instruction_bg_color = '#9400D3' ### DarkViolet
        self.game_phase.instruction.configure({'background': instruction_bg_color, 'foreground': ColorUtils.get_fg_from_bg(instruction_bg_color)})