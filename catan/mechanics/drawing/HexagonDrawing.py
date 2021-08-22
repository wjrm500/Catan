import math
from ...objects.board.Hexagon import Hexagon

class HexagonDrawing:
    @classmethod
    def draw_hexagons(cls, game):
        hexagons = []
        start_node = game.distributor.get_node(0, 0)
        hexagon = cls.draw_hexagon(game.distributor, start_node, 0)
        hexagons.append(hexagon)
        while len(hexagons) < game.num_hexagons:
            start_node = hexagon.last_free_node() if len(hexagons) > 1 else hexagon.nodes[2]
            start_angle = start_node.start_angle()
            hexagon = cls.draw_hexagon(game.distributor, start_node, start_angle)
            hexagons.append(hexagon)
        return hexagons

    @staticmethod
    def draw_hexagon(distributor, node, angle):
        lines, nodes = [], [node]
        while True:
            adj = math.cos(angle)
            opp = math.sin(angle)
            node_x = node.x + opp
            node_y = node.y + adj
            node = distributor.get_node(node_x, node_y)
            if node == nodes[0]:
                line = distributor.get_line(nodes[-1], nodes[0])
                lines.append(line)
                break
            line = distributor.get_line(nodes[-1], node)
            nodes.append(node)
            lines.append(line)
            angle += math.pi / 3
        return Hexagon(lines, nodes)