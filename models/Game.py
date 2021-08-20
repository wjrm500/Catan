import math
import random
import copy
from .Hexagon import Hexagon
from .Line import Line
from .Point import Point

class Game:
    def __init__(self, config, num_hexagons = 19):
        self.config = config
        self.num_hexagons = num_hexagons
        self.resources = self.set_resources()
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
            point = self.get_point(point_x, point_y)
            if point == points[0]:
                line = self.get_line(points[-1], points[0])
                lines.append(line)
                break
            line = self.get_line(points[-1], point)
            points.append(point)
            lines.append(line)
            angle += math.pi / 3
        resource_type = self.get_resource_type()
        hexagon = Hexagon(lines, points, resource_type)
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
    
    def set_resources(self):
        resources = ['desert']
        resource_types = copy.deepcopy(self.config['resource_types'])
        while len(resources) < self.num_hexagons:
            random_resource_type = random.choice(
                [resource_type for resource_type, info in resource_types.items() if info['count'] > 0])
            resources.append(random_resource_type)
            resource_types[random_resource_type]['count'] -= 1
            if sum([info['count'] for info in resource_types.values()]) == 0:
                resource_types = copy.deepcopy(self.config['resource_types'])
        random.shuffle(resources)
        return resources

    def get_resource_type(self):
        return self.resources.pop()