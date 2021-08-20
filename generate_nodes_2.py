### Hexagon builder
"""
Right 1

"""
import math
import itertools

from numpy.core.fromnumeric import transpose

cur_pos = {'x': 0, 'y': 0}
num_hexagons = 5
hexagons = []
starting_drawing_angle = math.pi / 6
while len(hexagons) < num_hexagons:
    points = []
    drawing_angle = starting_drawing_angle
    i = 0
    points.append(cur_pos)
    while True:
        adj = math.cos(drawing_angle) ### x_diff
        opp = math.sin(drawing_angle) ### y_diff
        cur_pos_x = cur_pos['x'] + adj
        cur_pos_y = cur_pos['y'] - opp
        cur_pos = {'x': cur_pos_x, 'y': cur_pos_y}
        points.append(cur_pos)
        if (round(cur_pos['x'], 5) == round(points[0]['x'], 5) and round(cur_pos['y'], 5) == round(points[0]['y'], 5)) or i > 6:
            break
        drawing_angle += math.pi / 3
        i += 1
    hexagons.append(points)
    cur_pos = hexagons[-1][-(len(hexagons) + 1)] ## SHOULD BE LAST POINT IN LAST HEXAGON THAT IS ONLY IN THAT HEXAGON
    starting_drawing_angle += math.pi if len(hexagons) == 1 else math.pi / 3 * 2

# points = []
# drawing_angle = math.pi / 6
# while True:
#     points.append(cur_pos)
#     hyp = side_len
#     adj = math.cos(drawing_angle) ### x_diff
#     opp = math.sin(drawing_angle) ### y_diff
#     cur_pos_x = cur_pos['x'] - adj
#     cur_pos_y = cur_pos['y'] - opp
#     cur_pos = {'x': cur_pos_x, 'y': cur_pos_y}
#     if round(cur_pos['x'], 5) == round(points[0]['x'], 5) and round(cur_pos['y'], 5) == round(points[0]['y'], 5):
#         break
#     drawing_angle += math.pi / 3

# cur_pos = {'x': 0, 'y': 0}
# drawing_angle = math.pi / 6 * 5
# while True:
#     points.append(cur_pos)
#     hyp = side_len
#     adj = math.cos(drawing_angle) ### x_diff
#     opp = math.sin(drawing_angle) ### y_diff
#     cur_pos_x = cur_pos['x'] - adj
#     cur_pos_y = cur_pos['y'] - opp
#     cur_pos = {'x': cur_pos_x, 'y': cur_pos_y}
#     if round(cur_pos['x'], 5) == round(points[0]['x'], 5) and round(cur_pos['y'], 5) == round(points[0]['y'], 5):
#         break
#     drawing_angle += math.pi / 3

for points in hexagons:
    print('New hex')
    for point in points:
        print([round(coord, 2) for coord in point.values()])

from matplotlib import pyplot as plt
fig, ax = plt.subplots()
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_aspect('equal', adjustable='box')
colors = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0], [0, 0, 0]]
original_circle_size, circle_size_decrement_factor = 0.2, 20
original_opacity, opacity_decrement_factor = 1, 20
for points, color in itertools.zip_longest(hexagons, colors):
    ax.plot([i['x'] for i in points], [i['y'] for i in points], color = color)
    for i, point in enumerate(points):
        circle_size = original_circle_size - i / circle_size_decrement_factor
        tranparentized_color = color.copy()
        transparentized_color = [0, 0, 0]
        tranparentized_color.append(original_opacity - i / opacity_decrement_factor)
        circle = plt.Circle([point['x'], point['y']], circle_size, color = tuple(tranparentized_color))
        ax.add_patch(circle)
plt.show()