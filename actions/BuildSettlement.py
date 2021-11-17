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

        ### Replace node in client distributor with settled node from server distributor
        ClientServerInterface.replace_object_in_distributor(hexagon_rendering.distributor, Distributor.OBJ_NODE, node)

        ### Building settlement
        x = node.real_x
        y = node.real_y
        hexagon_rendering.create_rectangle(x - r, y - r, x + r, y + r, tags = tags, fill = fill, width = width)