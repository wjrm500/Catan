import math

class Game:
    def __init__(self, num_hexagons):
        self.num_hexagons = num_hexagons
        self.hexagons = []
        self.lines = []
        self.points = []
    
    def draw_board(self):
        pass ### TODO: Implement

    def draw_hexagon(self, point, angle):
        lines, points = [], [point]
        while True:
            adj = math.cos(angle)
            opp = math.sin(angle)
            point_x = point.x + opp
            point_y = point.y + adj
            if round(point_x, 2) == 1.73 and round(point_y, 2) == 1:
                a = 1
            point = self.get_point(point_x, point_y)
            if point == points[0]:
                line = self.get_line(points[-1], points[0])
                lines.append(line)
                break
            line = self.get_line(points[-1], point)
            points.append(point)
            lines.append(line)
            angle += math.pi / 3
        hexagon = Hexagon(lines, points)
        self.hexagons.append(hexagon)
        return hexagon
    
    def get_point(self, x, y):
        for point in self.points:
            if point.test(x, y):
                return point
        point = Point(x, y)
        self.points.append(point)
        return point
    
    def get_line(self, start_point, end_point):
        for line in self.lines:
            if line.test(start_point, end_point):
                return line
        line = Line(start_point, end_point)
        self.lines.append(line)
        return line

class Hexagon:
    def __init__(self, lines, points):
        self.lines = lines
        self.points = points
        for line in self.lines:
            line.hexagons.append(self)
        for point in self.points:
            point.hexagons.append(self)
        
    def last_free_point(self):
        for point in self.points[::-1]:
            if len(point.lines) < 3:
                return point

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hexagons = []
        self.lines = []
    
    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return round(self.x, 2) == round(other.x, 2) and round(self.y, 2) == round(other.y, 2)
    
    def starting_angle(self):
        if len(self.lines) != 2:
            raise Exception('Starting angle can only be found if point is associated with two lines')
        # starting_angle = min([line.angle() for line in self.lines]) - math.pi / 3
        # return starting_angle if starting_angle > 0 else starting_angle + math.pi * 2
        angle = self.lines[0].angle()
        return angle - math.pi / 3 if angle > math.pi / 2 else angle + math.pi * 5 / 3

    def test(self, x, y):
        return round(self.x, 2) == round(x, 2) and round(self.y, 2) == round(y, 2)

class Line:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
        self.points = [self.start_point, self.end_point]
        for point in self.points:
            point.lines.append(self)
        self.hexagons = []
    
    def angle(self):
        y_change = self.end_point.y - self.start_point.y
        x_change = self.end_point.x - self.start_point.x
        angle = math.atan2(y_change, x_change)
        if angle > math.pi / 2:
            angle = math.pi * 5 / 2 - angle
        elif angle > 0:
            angle = math.pi / 2 - angle
        else:
            angle = math.pi / 2 + abs(angle)
        # print('X Change: {}\nY Change: {}\nAngle: {}\n\n'.format(
        #     round(x_change, 2),
        #     round(y_change, 2),
        #     round(angle)
        # ))
        return angle

    def test(self, start_point, end_point):
        return self.start_point == start_point and self.end_point == end_point

game = Game(19)
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
    for i, line in enumerate(hexagon.lines):
        color = 'red' if i == 0 else 'black'
        ax.plot([line.start_point.x, line.end_point.x], [line.start_point.y, line.end_point.y], color = color)
    # ax.plot([point.x for point in hexagon.points], [point.y for point in hexagon.points])
    circle = plt.Circle([hexagon.points[0].x, hexagon.points[0].y], 0.2, color = 'black')
    ax.add_patch(circle)
plt.show()