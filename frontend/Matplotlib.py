from matplotlib import pyplot as plt
import numpy as np

class Matplotlib():
    @staticmethod
    def draw_board(game, scale = 2):
        average_node_x_position = np.mean([node.x for node in game.distributor.nodes]) * scale
        average_node_y_position = np.mean([node.y for node in game.distributor.nodes]) * scale
        x_shift, y_shift = -average_node_x_position, -average_node_y_position
        _, ax = plt.subplots()
        ax.set_aspect('equal', adjustable = 'box')
        for hexagon in game.distributor.hexagons:
            nodes = hexagon.nodes + [hexagon.nodes[0]]
            port_nodes = [node for node in nodes if node.port]
            for port_node in port_nodes:
                port_type = port_node.port.type
                circle_color = '#0000FF' if port_type == 'general' else game.config['resource_types'][port_node.port.type]['color']
                circle = plt.Circle(
                    [port_node.x * scale + x_shift, port_node.y * scale + y_shift],
                    0.2,
                    color = circle_color
                )
                ax.add_patch(circle)
            ax.plot(
                [node.x * scale + x_shift for node in nodes],
                [node.y * scale + y_shift for node in nodes],
                color = 'black'
            )
        text_scale = ax.get_xlim()[1] / 10
        for hexagon in game.distributor.hexagons:
            text_dicts = [
                {
                    'font_size': round(16 / text_scale),
                    'font_weight': 'bold',
                    'text': hexagon.roll_num,
                    'y_shift': 0.5
                },
                {
                    'font_size': round(8 / text_scale),
                    'text': hexagon.resource_type,
                    'y_shift': -0.25
                },
                {
                    'font_size': round(12 / text_scale),
                    'text': ''.join(['·' for _ in range(hexagon.num_pips)]),
                    'y_shift': -0.75
                },
            ]
            for text_dict in text_dicts:
                plt.text(
                    hexagon.centre_point()[0] * scale + x_shift,
                    hexagon.centre_point()[1] * scale + y_shift + text_dict['y_shift'],
                    text_dict['text'],
                    fontsize = text_dict['font_size'],
                    fontweight = text_dict.get('font_weight', 'normal'),
                    ha = 'center',
                    va = 'center',
                    color = game.config['resource_types'][hexagon.resource_type]['color']
                )
        plt.axis('off')
        plt.show()