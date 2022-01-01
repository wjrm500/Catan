from actions.Action import Action
from backend.mechanics.Distributor import Distributor
from frontend.GeneralUtils import GeneralUtils as gutils
from frontend.Tkinter.rendering.HexagonRendering import HexagonRendering

class BuildRoad(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        self.chaperone = chaperone
        self.game_phase = self.chaperone.current_phase
        self.data = data
        self.hexagon_rendering = chaperone.current_phase.hexagon_rendering

        ### Following two lines necessary to work with client-side versions of objects
        line = self.hexagon_rendering.distributor.get_object_by_id(Distributor.OBJ_LINE, data['line_id'])
        road = self.hexagon_rendering.distributor.get_object_by_id(Distributor.OBJ_ROAD, data['road_id'])
        line.add_road(road)

        in_settling_phase = gutils.safe_isinstance(self.game_phase, 'SettlingPhase')
        if in_settling_phase:
            chaperone.current_phase.update_active_player_index()
        move_on_to_next_phase = sum([bool(settlement.node) for player in self.chaperone.players for settlement in player.settlements]) == len(self.chaperone.players) * 2
        if move_on_to_next_phase or not in_settling_phase:
            self.reload_all_players()
        self.update_gui(in_settling_phase, move_on_to_next_phase)
    
    def update_gui(self, in_settling_phase, move_on_to_next_phase):
        self.refresh_game_board()
        text_area = self.get_history_text_area(in_settling_phase)
        self.enable_text_area(text_area)

        if self.data['from_development_card'] and self.data['road_building_turn_index'] == 0:
            text_area.insert('end', f'\n\n{self.data["player"].name} played a Road Building card...', 'purple_font')

        ### X built a road
        text_to_insert = f'{self.data["player"].name} built a road.'
        text_area.insert('end', f'\n\n{text_to_insert}', 'green_font')

        if in_settling_phase:
            is_active = self.game_phase.client_active()
            if is_active:
                self.hexagon_rendering.canvas_mode = HexagonRendering.CANVAS_MODE_BUILD_VILLAGE
                self.game_phase.instruction_text.set('Build a village!')
                self.game_phase.instruction.configure({'background': '#90EE90'}) ### LightGreen
            else:
                self.hexagon_rendering.canvas_mode = HexagonRendering.CANVAS_MODE_DISABLED
                self.game_phase.instruction_text.set('Please wait for your turn')
                self.game_phase.instruction.configure({'background': '#F08080'}) ### LightCoral
            if move_on_to_next_phase:
                ### Move to main game phase prompt
                text_to_insert = f'The settling phase is now complete! The game creator should now click the "Proceed" button in the bottom right corner of their screen to advance all players to the main game.'
                text_area.insert('end', f'\n\n{text_to_insert}')
                self.hexagon_rendering.canvas_mode = HexagonRendering.CANVAS_MODE_DISABLED
                if self.chaperone.main:
                    self.game_phase.instruction_text.set('Press the "Proceed" button!')
                    self.game_phase.instruction.configure({'background': '#90EE90'}) ### LightGreen
                    self.game_phase.activate_button()
                else:
                    self.game_phase.instruction_text.set('Please wait for the game to begin...')
                    self.game_phase.instruction.configure({'background': '#F08080'}) ### LightCoral
            else:
                ### Round X commencing...
                at_start = self.game_phase.active_player_index == 0
                at_end = self.game_phase.active_player_index == len(self.chaperone.players) - 1
                commencing_at_start = at_start and self.game_phase.active_player_index_incrementing
                commencing_at_end = at_end and not self.game_phase.active_player_index_incrementing
                if commencing_at_start or commencing_at_end:
                    max_settlements = max(sum(bool(settlement.node) for settlement in player.settlements) for player in self.chaperone.players)
                    text_to_insert = f"Round {max_settlements + 1} commencing..."
                    text_area.insert('end', f'\n\n{text_to_insert}')

                ### It's X's turn to settle
                text_to_insert = f"It's {self.game_phase.active_player().name}'s turn to settle..."
                text_area.insert('end', f'\n\n{text_to_insert}')
        else: ### In main game phase
            if self.is_instigating_client():
                if self.data['from_development_card']:
                    if self.data['road_building_turn_index'] == 0:
                        self.game_phase.instruction_text.set('Build another road!')
                        play_frame_handler = self.game_phase.notebook_frame_handlers['play']
                        play_frame_handler.action_tree_handler.road_building_turn_index += 1
                    else:
                        self.refresh_play_frame_handler()
                else:
                    self.refresh_play_frame_handler()
            self.refresh_status_frame_handler()

        self.disable_text_area(text_area)