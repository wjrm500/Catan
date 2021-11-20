import math
import numpy as np

from config import config
from frontend.ColorUtils import ColorUtils
from frontend.GeneralUtils import GeneralUtils
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
        ### Below dicts are for keeping track of canvas objects when they are clicked
        self.rectangle_node_dict = {}
        self.line_dict = {}
    
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
        line_id = self.canvas.create_line(*args, **kwargs)
        self.update_canvas_object_count(self.CV_OBJ_LINE, self.ACTION_CREATE)
        return line_id
    
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
    
    def draw_board_items(self):
        self.draw_roads()
        self.draw_ports()
        self.draw_settlements()
    
    def handle_resize(self, event):
        try:
            self.canvas.pack(fill = 'both', expand = True)
            for hexagon in self.focused_hexagons:
                hexagon_render = self.hexagon_renders[hexagon.id]
                hexagon_render.unfocus()
            self.focused_hexagons = []
            self.draw_board()
            self.draw_board_items()
        except:
            pass
    
    def handle_motion(self, event):
        event_x, event_y = event.x, event.y
        if self.canvas_mode == self.CANVAS_MODE_BUILD_ROAD:
            self.handle_build_road_motion(event_x, event_y)
        elif self.canvas_mode == self.CANVAS_MODE_BUILD_SETTLEMENT:
            self.handle_build_settlement_motion(event_x, event_y)
        elif self.canvas_mode == self.CANVAS_MODE_DISABLED:
            pass
    
    def handle_leave(self, event):
        self.delete_tag(self.CT_OBJ_LINE)
        self.delete_tag(self.CT_OBJ_NODE)
        self.unfocus_focused_hexagons()
        self.draw_board_items()
        self.canvas.config(cursor = '')
        
    def handle_build_road_motion(self, event_x, event_y):
        self.canvas.config(cursor = '')
        self.delete_tag(self.CT_OBJ_LINE)

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
                res = np.sqrt(x * x + y * y)
            elif (AB_AE < 0):
                x, y = E[0] - A[0], E[1] - A[1]
                res = np.sqrt(x * x + y * y)
            else:
                x1, y1, x2, y2 = AB[0], AB[1], AE[0], AE[1]
                mod = np.sqrt(x1 * x1 + y1 * y1)
                res = abs(x1 * y2 - y1 * x2) / mod
            return res
        
        line_dists = [(line, get_dist_to_line(event_x, event_y, line)) for line in self.distributor.lines]
        min_line_dist = min(map(lambda x: x[1], line_dists))
        for line, dist in line_dists:
            closest_to_cursor = dist == min_line_dist
            if closest_to_cursor:
                reversed_dist = max(self.scale - dist, 0)
                fill_color = self.parent_phase.chaperone.player.color if min_line_dist / self.scale < 0.05 else 'black'
                line_width = min(self.scale * 3 / 4, reversed_dist) / 5
                draw_road_args = {'fill': fill_color, 'line': line, 'width': line_width}
                break
        
        line = draw_road_args['line']
        for node in line.nodes:
            current_phase = self.parent_phase.chaperone.current_phase
            node_settled = node.settlement and self.parent_phase.client_active()
            node_on_road = [line for line in node.lines if line.road and line.road.player is self.parent_phase.active_player()]
            if GeneralUtils.safe_isinstance(current_phase, 'SettlingPhase'):
                if node_settled and not node_on_road:
                    roadworthy = True; break
            elif GeneralUtils.safe_isinstance(current_phase, 'MainGamePhase'):
                if node_settled or node_on_road:
                    roadworthy = True; break
        else:
            roadworthy = False
        if not line.road:
            fill = draw_road_args['fill']
            width = draw_road_args['width']
            tags = [
                self.CT_OBJ_LINE,
                self.ct_line_tag(line),
                self.CV_OBJ_LINE
            ]
            x1, y1 = self.real_x(line.start_node), self.real_y(line.start_node)
            x2, y2 = self.real_x(line.end_node), self.real_y(line.end_node)
            outer_line_id = self.create_line(x1, y1, x2, y2, tags = tags, fill = 'black' if roadworthy else 'gray', width = width)
            if min_line_dist / self.scale < 0.05 and roadworthy:
                ### Draw coloured line to sit inside outer line so outer line appears to be a border
                x_shorten = (x2 - x1) / 25
                y_shorten = (y2 - y1) / 25
                new_x1 = x1 + x_shorten
                new_x2 = x2 - x_shorten
                new_y1 = y1 + y_shorten
                new_y2 = y2 - y_shorten
                inner_line_id = self.create_line(new_x1, new_y1, new_x2, new_y2, tags = tags, fill = fill, width = width * 0.6)

                ### Make clickable
                self.canvas.tag_bind(outer_line_id, '<Button-1>', self.handle_build_road_click)
                self.canvas.tag_bind(inner_line_id, '<Button-1>', self.handle_build_road_click)
                self.line_dict[outer_line_id] = line
                self.line_dict[inner_line_id] = line

                ### Show hand cursor to indicate clickability
                cursor = self.parent_phase.CURSOR_HAND
                self.canvas.config(cursor = cursor)

        self.draw_board_items()
    
    def handle_build_road_click(self, event):
        line_id = event.widget.find_withtag('current')[0]
        line = self.line_dict[line_id]
        self.parent_phase.chaperone.build_road(line)

    def handle_build_settlement_motion(self, event_x, event_y):
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
        self.draw_roads()
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
            self.canvas.tag_bind(rectangle_id, '<Button-1>', self.handle_build_settlement_click)
            self.rectangle_node_dict[rectangle_id] = node
        
            ### Change cursor pointer to hand icon if cursor near node
            cursor = self.parent_phase.CURSOR_HAND if min_node_dist / self.scale < 0.2 else ''
            self.canvas.config(cursor = cursor)
    
    def handle_build_settlement_click(self, event):
        rectangle_id = event.widget.find_withtag('current')[0]
        node = self.rectangle_node_dict[rectangle_id]
        self.parent_phase.chaperone.build_settlement(node)

    def unfocus_focused_hexagons(self):
        for hexagon in self.focused_hexagons:
            hexagon_render = self.hexagon_renders[hexagon.id]
            hexagon_render.unfocus()
        self.focused_hexagons = []
    
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
    
    ### TODO: Below methods crying out for merge
    def ct_line_tag(self, line):
        return '{}.{}'.format(self.CT_OBJ_LINE, line.id)
    
    def ct_hexagon_tag(self, hexagon):
        return '{}.{}'.format(self.CT_OBJ_HEXAGON, hexagon.id)

    def ct_node_tag(self, node):
        return '{}.{}'.format(self.CT_OBJ_NODE, node.id)
    
    def ct_port_tag(self, port):
        return '{}.{}'.format(self.CT_OBJ_PORT, port.id)
    
    def ct_road_tag(self, road):
        return '{}.{}'.format(self.CT_OBJ_ROAD, road.id)

    def ct_settlement_tag(self, settlement):
        return '{}.{}'.format(self.CT_OBJ_SETTLEMENT, settlement.id)
    
    def draw_roads(self):
        self.delete_tag(self.CT_OBJ_ROAD)
        for line in self.distributor.lines:
            if line.road:
                tags = [
                    self.CT_OBJ_ROAD,
                    self.ct_line_tag(line),
                    self.CV_OBJ_LINE
                ]
                x1, y1 = self.real_x(line.start_node), self.real_y(line.start_node)
                x2, y2 = self.real_x(line.end_node), self.real_y(line.end_node)
                width = (self.scale * 3 / 4) / 5
                self.create_line(x1, y1, x2, y2, tags = tags, fill = 'black', width = width)
                fill = line.road.player.color
                x_shorten = (x2 - x1) / 25
                y_shorten = (y2 - y1) / 25
                new_x1 = x1 + x_shorten
                new_x2 = x2 - x_shorten
                new_y1 = y1 + y_shorten
                new_y2 = y2 - y_shorten
                self.create_line(new_x1, new_y1, new_x2, new_y2, tags = tags, fill = fill, width = width * 0.6)

    def draw_ports(self, hovered_node = None, draw_node_args = None):
        self.delete_tag(self.CT_OBJ_PORT)
        port_nodes = [node for node in self.distributor.nodes if node.port]
        for port_node in port_nodes:
            if not hasattr(self, 'scale'):
                continue
            port_type = port_node.port.type
            circle_color = '#0000FF' if port_type == 'general' else BACKGROUND_COLORS[port_node.port.type]
            line_width = round(self.scale / 15)

            r = line_width * 2 ### Circle radius
            if hovered_node is not None and port_node is hovered_node and not port_node.adjacent_to_settled_node():
                r = max(r, draw_node_args['circle_radius'] * 2)
            if port_node.settlement:
                r = line_width * 5
            tags = [
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
        pct_canvas_used = 0.95
        return (node.x + (self.x_shift * 1 / pct_canvas_used)) * (self.scale * pct_canvas_used) + (self.x_centre_shift * 1 / pct_canvas_used)
    
    def real_y(self, node):
        pct_canvas_used = 0.95
        return (node.y + (self.y_shift * 1 / pct_canvas_used)) * (self.scale * pct_canvas_used) + (self.y_centre_shift * 1 / pct_canvas_used)