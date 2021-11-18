from ClientServerInterface import ClientServerInterface
from actions.Action import Action
from backend.mechanics.Distributor import Distributor

class BuildSettlement(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        hexagon_rendering = chaperone.current_phase.hexagon_rendering
        hexagon_rendering.delete_tag(hexagon_rendering.CT_OBJ_NODE)

        ### Following two lines necessary to work with client-side versions of objects
        node = hexagon_rendering.distributor.get_object_by_id(Distributor.OBJ_NODE, data['node'].id)
        settlement = hexagon_rendering.distributor.get_object_by_id(Distributor.OBJ_SETTLEMENT, data['settlement'].id)
        node.add_settlement(settlement)

        hexagon_rendering.draw_ports()
        hexagon_rendering.draw_settlements()
        hexagon_rendering.unfocus_focused_hexagons(None)
        hexagon_rendering.canvas_mode = hexagon_rendering.CANVAS_MODE_BUILD_ROAD
        hexagon_rendering.canvas.config(cursor = '')