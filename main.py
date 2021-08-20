from models.Game import Game
from config import config

game = Game(config, 30)
game.draw_board()

from matplotlib import pyplot as plt
fig, ax = plt.subplots()
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_aspect('equal', adjustable='box')
for hexagon in game.hexagons:
    points = hexagon.points + [hexagon.points[0]]
    port_points = [point for point in points if point.port_type]
    for port_point in port_points:
        port_type = port_point.port_type
        circle_color = 'blue' if port_type == 'any_resource' else config['resource_types'][port_point.port_type]['color']
        circle = plt.Circle(
            [port_point.x, port_point.y],
            0.2,
            color = circle_color
        )
        ax.add_patch(circle)
    ax.plot([point.x for point in points], [point.y for point in points], color = 'black')
    resource_type = hexagon.resource_type
    plt.text(
        hexagon.centre_point().x,
        hexagon.centre_point().y,
        resource_type,
        fontsize = 'xx-small',
        ha = 'center',
        va = 'center',
        color = config['resource_types'][hexagon.resource_type]['color']
    )
plt.show()