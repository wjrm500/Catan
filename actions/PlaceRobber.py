from actions.Action import Action
from backend.mechanics.Distributor import Distributor
from frontend.ColorUtils import ColorUtils
from frontend.Tkinter.phases.Phase import Phase
from frontend.Tkinter.rendering.HexagonRendering import HexagonRendering

class PlaceRobber(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        self.chaperone = chaperone
        self.game_phase = self.chaperone.current_phase
        self.data = data
        
        self.hexagon_rendering = chaperone.current_phase.hexagon_rendering

        ### Following three lines necessary to work with client-side versions of objects
        hexagon = self.hexagon_rendering.distributor.get_object_by_id(Distributor.OBJ_HEXAGON, data['hexagon'].id)
        robber = self.hexagon_rendering.distributor.robber
        robber.place_on_hexagon(hexagon)

        self.reload_all_players()

        self.update_gui()
    
    def update_gui(self):
        is_instigating_client = self.data['player'].id == self.chaperone.player.id
        if is_instigating_client:
            self.game_phase.hexagon_rendering.canvas_mode = HexagonRendering.CANVAS_MODE_DISABLED
            play_frame_handler = self.game_phase.notebook_frame_handlers['play']
            event_text = '\n'.join(self.data['text_events'])
            play_frame_handler.dice_roll_event_text.set(event_text)
            play_frame_handler.instruct_label.configure({'background': Phase.BG_COLOR})
            play_frame_handler.instruct_label.bind('<Motion>', lambda evt: play_frame_handler.root.configure(cursor = Phase.CURSOR_HAND))
            play_frame_handler.instruct_label.bind('<Leave>', lambda evt: play_frame_handler.root.configure(cursor = Phase.CURSOR_DEFAULT))
            button_function = play_frame_handler.transition_to_action_selection if play_frame_handler.instruct_label_text.get() == 'Take actions' else play_frame_handler.roll_dice
            play_frame_handler.instruct_label.bind('<Button-1>', button_function)
            self.game_phase.instruction_text.set("It's your turn!")
            instruction_bg_color = '#90EE90' ### LightGreen
            self.game_phase.instruction.configure({'background': instruction_bg_color, 'foreground': ColorUtils.get_fg_from_bg(instruction_bg_color)})
        else:
            self.refresh_play_frame_handler()
        self.refresh_game_board(full_refresh = True)
        text_area = self.get_text_area(in_settling_phase = False)
        self.enable_text_area(text_area)
        hexagon = self.data['hexagon']
        text_area.insert('end', f'\n\n{self.data["player"].name} placed the robber on a {hexagon.num_pips}-pip {hexagon.resource_type} hexagon!')
        self.disable_text_area(text_area)