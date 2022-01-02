from actions.Action import Action
from backend.mechanics.Distributor import Distributor

class MoveRobberToDesert(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        self.chaperone = chaperone
        self.game_phase = self.chaperone.current_phase
        self.data = data
        
        self.hexagon_rendering = chaperone.current_phase.hexagon_rendering

        ### Following three lines necessary to work with client-side versions of objects
        hexagon = self.hexagon_rendering.distributor.get_object_by_id(Distributor.OBJ_HEXAGON, data['hexagon_id'])
        robber = self.hexagon_rendering.distributor.robber
        robber.place_on_hexagon(hexagon)

        self.reload_all_players()
        self.update_gui()
    
    def update_gui(self):
        if self.is_instigating_client():
            self.refresh_play_frame_handler()
        self.refresh_game_board(full_refresh = True)
        text_area = self.get_history_text_area(in_settling_phase = False)
        text = f'\n\n{self.data["player"].name} moved the robber to the desert hex.'
        self.text_insert(text_area, text)