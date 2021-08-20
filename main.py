from models.Game import Game
from config import config

game = Game(config, 40)
starting_point = game.get_point(0, 0)
hexagon = game.draw_hexagon(starting_point, 0)
while len(game.hexagons) < game.num_hexagons:
    starting_point = hexagon.last_free_point() if len(game.hexagons) > 1 else hexagon.points[2]
    starting_angle = starting_point.starting_angle()
    hexagon = game.draw_hexagon(starting_point, starting_angle)

from matplotlib import pyplot as plt
fig, ax = plt.subplots()
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_aspect('equal', adjustable='box')
for hexagon in game.hexagons:

    points = hexagon.points + [hexagon.points[0]]
    ax.plot([point.x for point in points], [point.y for point in points], color = 'black')
    resource_type = hexagon.resource_type
    text_color = 'black' if resource_type == 'desert' else config['resource_types'][hexagon.resource_type]['color']
    plt.text(
        hexagon.centre_point().x,
        hexagon.centre_point().y,
        resource_type,
        fontsize = 'xx-small',
        ha = 'center',
        va = 'center',
        color = text_color
    )

    # for i, line in enumerate(hexagon.lines):
    #     color = 'red' if i == 0 else 'black'
    #     ax.plot([line.start_point.x, line.end_point.x], [line.start_point.y, line.end_point.y], color = color)
    # ax.plot([point.x for point in hexagon.points], [point.y for point in hexagon.points])
    # circle = plt.Circle([hexagon.points[0].x, hexagon.points[0].y], 0.2, color = 'black')
    # ax.add_patch(circle)
plt.show()