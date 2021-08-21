import math

class HexagonDrawing:
    @staticmethod
    def draw_hexagon(node, angle, distributor):
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
        return [lines, nodes]