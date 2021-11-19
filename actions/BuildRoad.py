from actions.Action import Action
from backend.mechanics.Distributor import Distributor
from frontend.GeneralUtils import GeneralUtils
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
        line = self.hexagon_rendering.distributor.get_object_by_id(Distributor.OBJ_LINE, data['line'].id)
        road = self.hexagon_rendering.distributor.get_object_by_id(Distributor.OBJ_ROAD, data['road'].id)
        line.add_road(road)

        in_settling_phase = GeneralUtils.safe_isinstance(self.game_phase, 'SettlingPhase')
        if in_settling_phase:
            chaperone.current_phase.update_active_player_index()
        self.update_gui(in_settling_phase)
    
    def update_gui(self, in_settling_phase):
        is_instigating_client = self.data['player'].id == self.chaperone.player.id
        is_active = self.chaperone.current_phase.client_active()
        if is_instigating_client:
            self.hexagon_rendering.handle_leave(event = None)
        else:
            self.hexagon_rendering.draw_board_items()
        if in_settling_phase:
            if is_active:
                self.hexagon_rendering.canvas_mode = HexagonRendering.CANVAS_MODE_BUILD_SETTLEMENT
                self.game_phase.instruction_text.set('Build a settlement!')
                self.game_phase.instruction.configure({'background': '#90EE90'}) ### LightGreen
            else:
                self.hexagon_rendering.canvas_mode = HexagonRendering.CANVAS_MODE_DISABLED
                self.game_phase.instruction_text.set('Please wait for your turn')
                self.game_phase.instruction.configure({'background': '#F08080'}) ### LightCoral