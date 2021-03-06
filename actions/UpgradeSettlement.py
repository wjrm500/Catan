from actions.Action import Action
from backend.mechanics.Distributor import Distributor

class UpgradeSettlement(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        self.chaperone = chaperone
        self.game_phase = self.chaperone.current_phase
        self.data = data
        self.hexagon_rendering = chaperone.current_phase.hexagon_rendering

        ### Following two lines necessary to work with client-side versions of objects
        node = self.hexagon_rendering.distributor.get_object_by_id(Distributor.OBJ_NODE, data['node_id'])
        city = self.hexagon_rendering.distributor.get_object_by_id(Distributor.OBJ_CITY, data['city_id'])
        node.add_city(city)

        self.reload_all_players() ### Not just active player because victory points etc. change
        self.update_gui()
    
    def update_gui(self):
        if self.is_instigating_client():
            self.hexagon_rendering.handle_leave(event = None)
        else:
            self.hexagon_rendering.draw_board_items()
        text_area = self.get_history_text_area(in_settling_phase = False)
        text = f'\n\n{self.data["player"].name} upgraded a village to a city!'
        self.text_insert(text_area, text, style = 'green_font')
        self.refresh_play_frame_handler()
        self.refresh_status_frame_handler()