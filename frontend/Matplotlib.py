from matplotlib import pyplot as plt

class Matplotlib():
    @staticmethod
    def draw_board(game):
        _, ax = plt.subplots()
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_aspect('equal', adjustable='box')
        for hexagon in game.hexagons:
            nodes = hexagon.nodes + [hexagon.nodes[0]]
            port_nodes = [node for node in nodes if node.port]
            for port_node in port_nodes:
                port_type = port_node.port.type
                circle_color = 'blue' if port_type == 'any_resource' else game.config['resource_types'][port_node.port.type]['color']
                circle = plt.Circle(
                    [port_node.x, port_node.y],
                    0.2,
                    color = circle_color
                )
                ax.add_patch(circle)
            ax.plot([node.x for node in nodes], [node.y for node in nodes], color = 'black')
            resource_type = hexagon.resource_type
            plt.text(
                hexagon.centre_point()[0],
                hexagon.centre_point()[1],
                resource_type,
                fontsize = 'xx-small',
                ha = 'center',
                va = 'center',
                color = game.config['resource_types'][hexagon.resource_type]['color']
            )
        plt.show()