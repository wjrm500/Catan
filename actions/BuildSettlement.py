from actions.Action import Action

class BuildSettlement(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        # chaperone.distributor = data['distributor']
        hexagon_rendering = chaperone.current_phase.hexagon_rendering
        hexagon_rendering.delete_tag(hexagon_rendering.CT_OBJ_NODE)
        tags = [
            hexagon_rendering.CT_OBJ_SETTLEMENT,
            # hexagon_rendering.ct_node_tag(node),
            hexagon_rendering.CV_OBJ_RECT
        ]
        r = (hexagon_rendering.scale * 3 / 4) / 5 ### Circle radius
        fill = chaperone.player.color
        width = (hexagon_rendering.scale * 3 / 4) / 10
        node = data['node']
        x, y = hexagon_rendering.real_x(node), hexagon_rendering.real_y(node)
        hexagon_rendering.create_rectangle(x - r, y - r, x + r, y + r, tags = tags, fill = fill, width = width)