from ClientServerInterface import ClientServerInterface
from actions.Action import Action
from backend.mechanics.Distributor import Distributor

class BuildSettlement(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        hexagon_rendering = chaperone.current_phase.hexagon_rendering
        hexagon_rendering.delete_tag(hexagon_rendering.CT_OBJ_NODE)
        tags = [
            hexagon_rendering.CT_OBJ_SETTLEMENT,
            # hexagon_rendering.ct_node_tag(node),
            hexagon_rendering.CV_OBJ_RECT
        ]
        r = (hexagon_rendering.scale * 3 / 4) / 5 ### Circle radius
        player = chaperone.get_player_from_id(data['player_id'])
        fill = player.color
        width = (hexagon_rendering.scale * 3 / 4) / 10
        node = data['node']
        settlement = data['settlement']

        ### Following two lines necessary to work with client-side versions of objects
        node = hexagon_rendering.distributor.get_object_by_id(Distributor.OBJ_NODE, node.id)
        settlement = hexagon_rendering.distributor.get_object_by_id(Distributor.OBJ_SETTLEMENT, settlement.id)
        node.add_settlement(settlement)

        ### Building settlement
        x = hexagon_rendering.real_x(node)
        y = hexagon_rendering.real_y(node)
        hexagon_rendering.create_rectangle(x - r, y - r, x + r, y + r, tags = tags, fill = fill, width = width)