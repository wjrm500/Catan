from frontend.Tkinter.rendering.HexagonRender import HexagonRender
import math

class HexagonRendering:
    OBJECT_LINE = 'line'
    OBJECT_POLYGON = 'polygon'
    OBJECT_OVAL = 'oval'
    OBJECT_TEXT = 'text'

    ACTION_CREATE = 'create'
    ACTION_DELETE = 'delete'

    def __init__(self, main_phase):
        self.main_phase = main_phase
        self.canvas = self.main_phase.canvas
        self.scale = 1
        self.focused_hexagons = []
        self.reset_canvas_objects()
    
    def reset_canvas_objects(self):
        self.canvas_objects = {
            self.OBJECT_LINE: 0,
            self.OBJECT_POLYGON: 0,
            self.OBJECT_OVAL: 0,
            self.OBJECT_TEXT: 0
        }
    
    def update_canvas_object_count(self, object_type, action_type, step = 1):
        if action_type == self.ACTION_DELETE:
            step *= -1
        self.canvas_objects[object_type] += step
        print(self.canvas_objects)
    
    def create_line(self, *args, **kwargs):
        self.canvas.create_line(*args, **kwargs)
        self.update_canvas_object_count(self.OBJECT_LINE, self.ACTION_CREATE)
    
    def create_polygon(self, *args, **kwargs):
        self.canvas.create_polygon(*args, **kwargs)
        self.update_canvas_object_count(self.OBJECT_POLYGON, self.ACTION_CREATE)
    
    def create_oval(self, *args, **kwargs):
        self.canvas.create_oval(*args, **kwargs)
        self.update_canvas_object_count(self.OBJECT_OVAL, self.ACTION_CREATE)
    
    def create_text(self, *args, **kwargs):
        self.canvas.create_text(*args, **kwargs)
        self.update_canvas_object_count(self.OBJECT_TEXT, self.ACTION_CREATE)
    
    def delete_tag(self, tag):
        ### TODO: DOES NOT WORK PROPERLY AS HEXAGON TAG PASSED IN FOR BOTH TEXT + POLYGONS
        object_type = tag.split('.')[0]
        object_count = len(self.canvas.find_withtag(tag))
        self.canvas.delete(tag)
        self.update_canvas_object_count(object_type, self.ACTION_DELETE, object_count)
    
    def set_scale(self, scale):
        self.scale = scale
    
    def render(self, hexagon, focused = False):
        hexagon_render = HexagonRender(self, hexagon)
        hexagon_render.set_focused(focused)
        hexagon_render.render()
    
    def handle_resize(self, event):
        self.canvas.pack(fill = "both", expand = True)
        for hexagon in self.focused_hexagons:
            hexagon_render = HexagonRender(self, hexagon)
            hexagon_render.border_render.remove_hexagon_border()
        self.focused_hexagons = []
        self.draw_board()
    
    def reset_focused_hexagons(self, event):
        for hexagon in self.focused_hexagons:
            hexagon_render = HexagonRender(self, hexagon)
            hexagon_render.border_render.remove_hexagon_border()
        self.focused_hexagons = []
        self.draw_board()
    
    def focus_hexagons(self, event):
        ### TODO: Refactor

        ########################
        # Reset canvas objects #
        ########################
        
        self.delete_tag(self.OBJECT_OVAL)

        ##########################################
        # Calculate arguments for canvas objects #
        ##########################################

        x1 = event.x
        y1 = event.y

        node_dists = [(node, math.sqrt(pow(node.real_x - x1, 2) + pow(node.real_y - y1, 2))) for node in self.game.distributor.nodes]
        min_node_dist = min(map(lambda x: x[1], node_dists))
        draw_tk_oval_args_list = []
        for node, dist in node_dists:
            closest_to_cursor = dist == min_node_dist
            reversed_dist = max(self.scale - dist, 0)
            if closest_to_cursor:
                hexagons_to_focus = [hexagon for hexagon in node.hexagons]
                circle_radius = reversed_dist / 5
                fill_color = 'limegreen' if dist / self.scale < 0.2 else 'white'
                line_width = reversed_dist / 10
                draw_tk_oval_args_list.append({'node': node, 'circle_radius': circle_radius, 'fill': fill_color, 'width': line_width})
        
        ################################
        # Actually draw canvas objects #
        ################################

        for hexagon in self.focused_hexagons:
            if hexagon not in hexagons_to_focus:
                hexagon_render = HexagonRender(self, hexagon)
                hexagon_render.unfocus(hexagons_to_focus)
        
        self.focused_hexagons = [hexagon for hexagon in self.focused_hexagons if hexagon in hexagons_to_focus]

        for hexagon in hexagons_to_focus:
            if hexagon not in self.focused_hexagons:
                focused = True
                self.render(hexagon, focused)
                self.focused_hexagons.append(hexagon)

        for args in draw_tk_oval_args_list:
            self.draw_tk_oval(args['node'], args['circle_radius'], fill = args['fill'], width = args['width'])
        
        cursor = self.main_phase.CURSOR_HAND if min_node_dist / self.scale < 0.2 else ''
        self.canvas.config(cursor = cursor)
    
    def draw_tk_oval(self, node, circle_radius, fill = 'white', width = 1):
        self.create_oval(node.real_x - circle_radius, node.real_y - circle_radius, node.real_x + circle_radius, node.real_y + circle_radius, tags = self.OBJECT_OVAL, fill = fill, width = width)
    
    def draw_board(self):
        ### TODO: Refactor
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        if self.canvas_width > 11: ### Width on initial render before resize
            self.canvas.delete('all')
            self.reset_canvas_objects()
            node_x_values = [node.x for node in self.game.distributor.nodes]
            node_y_values = [node.y for node in self.game.distributor.nodes]
            x_shift = -min(node_x_values)
            y_shift = -min(node_y_values)
            x_max = max(node_x_values) + x_shift
            y_max = max(node_y_values) + y_shift
            canvas_x_max_ratio = self.canvas_width / x_max
            canvas_y_max_ratio = self.canvas_height / y_max
            self.scale = min(canvas_x_max_ratio, canvas_y_max_ratio) * 0.95
            x_centre_shift = (self.canvas_width - x_max * self.scale) / 2
            y_centre_shift = (self.canvas_height - y_max * self.scale) / 2
            self.centre_points = []

            for node in self.game.distributor.nodes:
                node.real_x = (node.x + x_shift) * self.scale + x_centre_shift
                node.real_y = (node.y + y_shift) * self.scale + y_centre_shift

            for hexagon in self.game.distributor.hexagons:
                self.render(hexagon)