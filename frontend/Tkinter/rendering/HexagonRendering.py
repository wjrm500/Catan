import math
import numpy as np
from numpy.linalg import norm
import random

from config import config
from frontend.ColorUtils import ColorUtils
from frontend.Tkinter.rendering.HexagonRender import HexagonRender

def set_colors(darken): ### TODO: Factor out - duplicate on HexagonBodyRender
    d = {}
    for resource_type, data in config['resource_types'].items():
        d[resource_type] = ColorUtils.darken_hex(data['color'], darken)
    return d

BACKGROUND_COLORS = set_colors(0.0)

class HexagonRendering:
    ### Catan object constants
    CT_OBJ_HEXAGON = 'ct_hexagon'
    CT_OBJ_LINE = 'ct_line'
    CT_OBJ_NODE = 'ct_node'
    CT_OBJ_PORT = 'ct_port'
    CT_OBJ_ROAD = 'ct_road'
    CT_OBJ_SETTLEMENT = 'ct_settlement'

    ### Canvas object constants
    CV_OBJ_LINE = 'cv_line'
    CV_OBJ_POLYGON = 'cv_polygon'
    CV_OBJ_OVAL = 'cv_oval'
    CV_OBJ_RECT = 'cv_rectangle'
    CV_OBJ_TEXT = 'cv_text'

    ### Action constants
    ACTION_CREATE = 'create'
    ACTION_DELETE = 'delete'

    ### Canvas modes
    CANVAS_MODE_BUILD_ROAD = 'build_road'
    CANVAS_MODE_BUILD_SETTLEMENT = 'build_settlement'
    CANVAS_MODE_CITY_UPGRADE = 'city_upgrade'
    CANVAS_MODE_DEFAULT = 'default'
    CANVAS_MODE_DISABLED = 'disabled'
    
    IN_DEVELOPMENT = False

    def __init__(self, parent_phase):
        self.parent_phase = parent_phase
        self.canvas = self.parent_phase.canvas
        self.canvas_mode = self.CANVAS_MODE_DEFAULT
        self.scale = 1
        self.focused_hexagons = []
        self.reset_canvas_objects()
        self.distributor = self.parent_phase.chaperone.distributor
        self.hexagon_renders = {hexagon.id: HexagonRender(self, hexagon) for hexagon in self.distributor.hexagons}
        self.rectangle_node_dict = {}
    
    def reset_canvas_objects(self):
        self.canvas_objects = {
            self.CV_OBJ_LINE: 0,
            self.CV_OBJ_POLYGON: 0,
            self.CV_OBJ_OVAL: 0,
            self.CV_OBJ_RECT: 0,
            self.CV_OBJ_TEXT: 0
        }
    
    def update_canvas_object_count(self, object_type, action_type):
        step = 1 if action_type == self.ACTION_CREATE else -1 
        self.canvas_objects[object_type] += step
        if self.IN_DEVELOPMENT:
            print(self.canvas_objects)
    
    def create_line(self, *args, **kwargs):
        self.canvas.create_line(*args, **kwargs)
        self.update_canvas_object_count(self.CV_OBJ_LINE, self.ACTION_CREATE)
    
    def create_polygon(self, *args, **kwargs):
        self.canvas.create_polygon(*args, **kwargs)
        self.update_canvas_object_count(self.CV_OBJ_POLYGON, self.ACTION_CREATE)
    
    def create_oval(self, *args, **kwargs):
        self.canvas.create_oval(*args, **kwargs)
        self.update_canvas_object_count(self.CV_OBJ_OVAL, self.ACTION_CREATE)
    
    def create_rectangle(self, *args, **kwargs):
        rectangle_id = self.canvas.create_rectangle(*args, **kwargs)
        self.update_canvas_object_count(self.CV_OBJ_RECT, self.ACTION_CREATE)
        return rectangle_id
    
    def create_text(self, *args, **kwargs):
        self.canvas.create_text(*args, **kwargs)
        self.update_canvas_object_count(self.CV_OBJ_TEXT, self.ACTION_CREATE)
    
    def delete_tag(self, tag):
        if not self.IN_DEVELOPMENT:
            self.canvas.delete(tag)
        else:
            objects_with_tag = self.canvas.find_withtag(tag)
            for object_with_tag in objects_with_tag:
                all_tags_on_object = self.canvas.itemcget(object_with_tag, 'tags')
                for key in self.canvas_objects.keys():
                    if key in all_tags_on_object:
                        object_type = key
                        self.canvas.delete(object_with_tag)
                        self.update_canvas_object_count(object_type, self.ACTION_DELETE)
    
    def set_scale(self, scale):
        self.scale = scale
    
    def init_render(self, hexagon):
        hexagon_render = self.hexagon_renders[hexagon.id]
        hexagon_render.init_render()
    
    def focus(self, hexagon):
        hexagon_render = self.hexagon_renders[hexagon.id]
        hexagon_render.focus()
    
    def unfocus(self, hexagon, hexagons_to_focus):
        hexagon_render = self.hexagon_renders[hexagon.id]
        hexagon_render.unfocus(hexagons_to_focus)
    
    def handle_resize(self, event):
        self.canvas.pack(fill = "both", expand = True)
        for hexagon in self.focused_hexagons:
            hexagon_render = self.hexagon_renders[hexagon.id]
            hexagon_render.unfocus()
        self.focused_hexagons = []
        self.draw_board()
        self.draw_ports()
        self.draw_settlements()
    
    def handle_motion(self, event):
        event_x, event_y = event.x, event.y
        if self.canvas_mode == self.CANVAS_MODE_BUILD_ROAD:
            self.build_road(event_x, event_y)
        elif self.canvas_mode == self.CANVAS_MODE_BUILD_SETTLEMENT:
            self.build_settlement(event_x, event_y)
        elif self.canvas_mode == self.CANVAS_MODE_DISABLED:
            pass
        
    def build_road(self, event_x, event_y):
        self.delete_tag(self.CT_OBJ_ROAD)

        ### Find closest line to cursor
        def get_dist_to_line(event_x, event_y, line): ### https://www.geeksforgeeks.org/minimum-distance-from-a-point-to-the-line-segment-using-vectors/
            E = event_x, event_y
            A = self.real_x(line.start_node), self.real_y(line.start_node)
            B = self.real_x(line.end_node), self.real_y(line.end_node)
            AB = [B[0] - A[0], B[1] - A[1]]
            BE = [E[0] - B[0], E[1] - B[1]] 
            AE = [E[0] - A[0], E[1] - A[1]]
            AB_BE = AB[0] * BE[0] + AB[1] * BE[1]
            AB_AE = AB[0] * AE[0] + AB[1] * AE[1]
            if (AB_BE > 0):
                x, y = E[0] - B[0], E[1] - B[1]
                reqAns = np.sqrt(x * x + y * y)
            elif (AB_AE < 0):
                x, y = E[0] - A[0], E[1] - A[1]
                reqAns = np.sqrt(x * x + y * y)
            else:
                x1, y1, x2, y2 = AB[0], AB[1], AE[0], AE[1]
                mod = np.sqrt(x1 * x1 + y1 * y1)
                reqAns = abs(x1 * y2 - y1 * x2) / mod
            return reqAns
        
        line_dists = [(line, get_dist_to_line(event_x, event_y, line)) for line in self.distributor.lines]
        min_line_dist = min(map(lambda x: x[1], line_dists))
        for line, dist in line_dists:
            closest_to_cursor = dist == min_line_dist
            if closest_to_cursor:
                reversed_dist = max(self.scale - dist, 0)
                fill_color = self.parent_phase.chaperone.player.color if min_line_dist / self.scale < 0.2 else 'white'
                line_width = min(self.scale * 3 / 4, reversed_dist) / 10
                draw_road_args = {'fill': fill_color, 'line': line, 'width': line_width}
                break
        
        line = draw_road_args['line']
        if not line.road:
            # r = draw_node_args['circle_radius']
            # fill = draw_node_args['fill']
            # width = draw_node_args['width']
            tags = [
                self.CT_OBJ_ROAD,
                # self.ct_node_tag(node),
                # self.CV_OBJ_RECT
            ]
            x1, y1 = self.real_x(line.start_node), self.real_y(line.start_node)
            x2, y2 = self.real_x(line.end_node), self.real_y(line.end_node)
            line_id = self.create_line(x1, y1, x2, y2, tags = tags, width = 10)# fill: fill,
            # self.canvas.tag_bind(rectangle_id, '<Button-1>', self.handle_click)
            # self.rectangle_node_dict[rectangle_id] = node
        
            # ### Change cursor pointer to hand icon if cursor near node
            # cursor = self.parent_phase.CURSOR_HAND if min_node_dist / self.scale < 0.2 else ''
            # self.canvas.config(cursor = cursor)

    def build_settlement(self, event_x, event_y):
        self.delete_tag(self.CT_OBJ_NODE)

        ### Find closest node to cursor and collect arguments for rendering
        get_dist_to_node = lambda node: math.sqrt(pow(self.real_x(node) - event_x, 2) + pow(self.real_y(node) - event_y, 2))
        node_dists = [(node, get_dist_to_node(node)) for node in self.distributor.nodes]
        min_node_dist = min(map(lambda x: x[1], node_dists))
        for node, dist in node_dists:
            closest_to_cursor = dist == min_node_dist
            if closest_to_cursor:
                reversed_dist = max(self.scale - dist, 0)
                hexagons_to_focus = [hexagon for hexagon in node.hexagons]
                circle_radius = min(self.scale * 3 / 4, reversed_dist) / 5
                fill_color = self.parent_phase.chaperone.player.color if min_node_dist / self.scale < 0.2 else 'white'
                line_width = min(self.scale * 3 / 4, reversed_dist) / 10
                draw_node_args = {'node': node, 'circle_radius': circle_radius, 'fill': fill_color, 'width': line_width}
                break
        
        ### Focus / unfocus hexagons
        for hexagon in self.focused_hexagons:
            if hexagon not in hexagons_to_focus:
                hexagon_render = self.hexagon_renders[hexagon.id]
                hexagon_render.unfocus(hexagons_to_focus)
        self.focused_hexagons = [hexagon for hexagon in self.focused_hexagons if hexagon in hexagons_to_focus]
        for hexagon in hexagons_to_focus:
            if hexagon not in self.focused_hexagons:
                hexagon_render = self.hexagon_renders[hexagon.id]
                hexagon_render.focus()
                self.focused_hexagons.append(hexagon)
        
        ### TODO: Run the following methods more efficiently - ONLY REDRAW PORTS AND SETTLEMENTS AFFECTED BY HEXAGON FOCUSING
        self.draw_ports(node, draw_node_args)
        self.draw_settlements()

        node = draw_node_args['node']
        if not node.settlement and not node.adjacent_to_settled_node():
            ### Draw node (must come after hexagon drawing, hence the separation of argument collection and rendering)
            r = draw_node_args['circle_radius']
            fill = draw_node_args['fill']
            width = draw_node_args['width']
            tags = [
                self.CT_OBJ_NODE,
                self.ct_node_tag(node),
                self.CV_OBJ_RECT
            ]
            x, y = self.real_x(node), self.real_y(node)
            rectangle_id = self.create_rectangle(x - r, y - r, x + r, y + r, tags = tags, fill = fill, width = width)
            self.canvas.tag_bind(rectangle_id, '<Button-1>', self.handle_click)
            self.rectangle_node_dict[rectangle_id] = node
        
            ### Change cursor pointer to hand icon if cursor near node
            cursor = self.parent_phase.CURSOR_HAND if min_node_dist / self.scale < 0.2 else ''
            self.canvas.config(cursor = cursor)
    
    def handle_click(self, event):
        rectangle_id = event.widget.find_withtag('current')[0]
        node = self.rectangle_node_dict[rectangle_id]
        self.parent_phase.chaperone.build_settlement(node)

    def unfocus_focused_hexagons(self, event):
        for hexagon in self.focused_hexagons:
            hexagon_render = self.hexagon_renders[hexagon.id]
            hexagon_render.unfocus()
        self.focused_hexagons = []
        self.draw_ports()
        self.draw_settlements()
    
    def draw_board(self):
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        if self.canvas_width > 11: ### Width on initial render before resize
            self.canvas.delete('all')
            self.reset_canvas_objects()
            node_x_values = [node.x for node in self.distributor.nodes]
            node_y_values = [node.y for node in self.distributor.nodes]
            self.x_shift = -min(node_x_values)
            self.y_shift = -min(node_y_values)
            x_max = max(node_x_values) + self.x_shift
            y_max = max(node_y_values) + self.y_shift
            canvas_x_max_ratio = self.canvas_width / x_max
            canvas_y_max_ratio = self.canvas_height / y_max
            self.scale = min(canvas_x_max_ratio, canvas_y_max_ratio) * 0.95
            self.x_centre_shift = (self.canvas_width - x_max * self.scale) / 2
            self.y_centre_shift = (self.canvas_height - y_max * self.scale) / 2
            self.centre_points = []
            for hexagon in self.distributor.hexagons:
                self.init_render(hexagon)
    
    def ct_line_tag(self, line):
        return '{}.{}'.format(self.CT_OBJ_LINE, line.id)
    
    def ct_hexagon_tag(self, hexagon):
        return '{}.{}'.format(self.CT_OBJ_HEXAGON, hexagon.id)

    def ct_node_tag(self, node):
        return '{}.{}'.format(self.CT_OBJ_NODE, node.id)
    
    def ct_port_tag(self, port):
        return '{}.{}'.format(self.CT_OBJ_PORT, port.id)
    
    def ct_settlement_tag(self, settlement):
        return '{}.{}'.format(self.CT_OBJ_SETTLEMENT, settlement.id)

    def draw_ports(self, hovered_node = None, draw_node_args = None):
        self.delete_tag(self.CT_OBJ_PORT)
        port_nodes = [node for node in self.distributor.nodes if node.port]
        for port_node in port_nodes:
            if not hasattr(self, 'scale'):
                continue
            port_type = port_node.port.type
            circle_color = '#87CEFA' if port_type == 'any_resource' else BACKGROUND_COLORS[port_node.port.type]
            line_width = round(self.scale / 15)

            r = line_width * 2 ### Circle radius
            if hovered_node is not None and port_node is hovered_node:
                r = max(r, draw_node_args['circle_radius'] * 2)
            if port_node.settlement:
                r = line_width * 5
            tags = [ ### TODO: Change these - do we need a new port tag?
                self.CT_OBJ_PORT,
                self.ct_port_tag(port_node),
                self.CV_OBJ_OVAL
            ]
            x, y = self.real_x(port_node), self.real_y(port_node)
            self.create_oval(x - r, y - r, x + r, y + r, tags = tags, fill = circle_color, outline = ColorUtils.darken_hex(circle_color, 0.5), width = line_width)
    
    def draw_settlements(self):
        self.delete_tag(self.CT_OBJ_SETTLEMENT)
        for node in self.distributor.nodes:
            if node.settlement:
                tags = [
                    self.CT_OBJ_SETTLEMENT,
                    self.ct_settlement_tag(node.settlement),
                    self.CV_OBJ_RECT
                ]
                r = (self.scale * 3 / 4) / 5 ### Circle radius
                fill = node.settlement.player.color
                width = (self.scale * 3 / 4) / 10
                x, y = self.real_x(node), self.real_y(node)
                self.create_rectangle(x - r, y - r, x + r, y + r, tags = tags, fill = fill, width = width)
    
    def real_x(self, node):
        scale_factor = 0.95
        # return (node.x + self.x_shift) * self.scale + self.x_centre_shift
        return (node.x + (self.x_shift * 1 / scale_factor)) * (self.scale * scale_factor) + (self.x_centre_shift * 1 / scale_factor)
    
    def real_y(self, node):
        scale_factor = 0.95
        # return (node.y + self.y_shift) * self.scale + self.y_centre_shift
        return (node.y + (self.y_shift * 1 / scale_factor)) * (self.scale * scale_factor) + (self.y_centre_shift * 1 / scale_factor)