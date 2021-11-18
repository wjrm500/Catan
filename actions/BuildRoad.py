from actions.Action import Action
from backend.mechanics.Distributor import Distributor
from frontend.Tkinter.phases.game.sub_phases.SettlingPhase import SettlingPhase

class BuildRoad(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        hexagon_rendering = chaperone.current_phase.hexagon_rendering
        # hexagon_rendering.delete_tag(hexagon_rendering.CT_OBJ_NODE)

        ### Following two lines necessary to work with client-side versions of objects
        line = hexagon_rendering.distributor.get_object_by_id(Distributor.OBJ_LINE, data['line'].id)
        road = hexagon_rendering.distributor.get_object_by_id(Distributor.OBJ_ROAD, data['road'].id)
        line.add_road(road)

        hexagon_rendering.draw_roads()
        hexagon_rendering.draw_ports()
        hexagon_rendering.draw_settlements()
        hexagon_rendering.unfocus_focused_hexagons(None)
        hexagon_rendering.canvas.config(cursor = '')
        if isinstance(chaperone.current_phase, SettlingPhase):
            chaperone.update_active_player_index()