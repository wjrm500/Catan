from frontend.Tkinter.rendering.HexagonRender import HexagonRender
import math

class HexagonRendering:
    ### Catan object constants
    CT_OBJ_HEXAGON = 'ct_hexagon'
    CT_OBJ_LINE = 'ct_line'
    CT_OBJ_NODE = 'ct_node'

    ### Canvas object constants
    CV_OBJ_LINE = 'cv_line'
    CV_OBJ_POLYGON = 'cv_polygon'
    CV_OBJ_OVAL = 'cv_oval'
    CV_OBJ_TEXT = 'cv_text'

    ### Action constants
    ACTION_CREATE = 'create'
    ACTION_DELETE = 'delete'

    def __init__(self, main_phase):
        self.main_phase = main_phase
        self.canvas = self.main_phase.canvas
        self.scale = 1
        self.focused_hexagons = []
        self.reset_canvas_objects()
    
    def set_game(self, game):
        self.game = game
        self.hexagon_renders = {hexagon.id: HexagonRender(self, hexagon) for hexagon in game.distributor.hexagons}
    
    def reset_canvas_objects(self):
        self.canvas_objects = {
            self.CV_OBJ_LINE: 0,
            self.CV_OBJ_POLYGON: 0,
            self.CV_OBJ_OVAL: 0,
            self.CV_OBJ_TEXT: 0
        }
    
    def update_canvas_object_count(self, object_type, action_type):
        step = 1 if action_type == self.ACTION_CREATE else -1 
        self.canvas_objects[object_type] += step
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
    
    def create_text(self, *args, **kwargs):
        self.canvas.create_text(*args, **kwargs)
        self.update_canvas_object_count(self.CV_OBJ_TEXT, self.ACTION_CREATE)
    
    def delete_tag(self, tag):
        self.canvas.delete(tag)
        # objects_with_tag = self.canvas.find_withtag(tag)
        # is_broken = False
        # for object_with_tag in objects_with_tag:
        #     all_tags_on_object = self.canvas.itemcget(object_with_tag, 'tags')
        #     for key in self.canvas_objects.keys():
        #         if key in all_tags_on_object:
        #             object_type = key
        #             self.canvas.delete(object_with_tag)
        #             self.update_canvas_object_count(object_type, self.ACTION_DELETE)
        #             is_broken = True
        #             break
        #     if is_broken:
                # break
    
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
    
    def handle_motion(self, event):
        self.delete_tag(self.CT_OBJ_NODE)

        ### Find closest node to cursor and collect arguments for rendering
        x1 = event.x
        y1 = event.y
        node_dists = [(node, math.sqrt(pow(node.real_x - x1, 2) + pow(node.real_y - y1, 2))) for node in self.game.distributor.nodes]
        min_node_dist = min(map(lambda x: x[1], node_dists))
        for node, dist in node_dists:
            closest_to_cursor = dist == min_node_dist
            if closest_to_cursor:
                reversed_dist = max(self.scale - dist, 0)
                hexagons_to_focus = [hexagon for hexagon in node.hexagons]
                circle_radius = reversed_dist / 5
                fill_color = 'limegreen' if min_node_dist / self.scale < 0.2 else 'white'
                line_width = reversed_dist / 10
                draw_oval_args = {'node': node, 'circle_radius': circle_radius, 'fill': fill_color, 'width': line_width}
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

        ### Draw node (must come after hexagon drawing, hence the separation of argument collection and rendering)
        node = draw_oval_args['node']
        circle_radius = draw_oval_args['circle_radius']
        fill = draw_oval_args['fill']
        width = draw_oval_args['width']
        tags = [
            self.CT_OBJ_NODE,
            self.ct_node_tag(node),
            self.CV_OBJ_OVAL
        ]
        self.create_oval(node.real_x - circle_radius, node.real_y - circle_radius, node.real_x + circle_radius, node.real_y + circle_radius, tags = tags, fill = fill, width = width)
        
        ### Change cursor pointer to hand icon if cursor near node
        cursor = self.main_phase.CURSOR_HAND if min_node_dist / self.scale < 0.2 else ''
        self.canvas.config(cursor = cursor)
    
    def unfocus_focused_hexagons(self, event):
        for hexagon in self.focused_hexagons:
            hexagon_render = self.hexagon_renders[hexagon.id]
            hexagon_render.unfocus()
        self.focused_hexagons = []    
    
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
                self.init_render(hexagon)
    
    def ct_line_tag(self, line):
        return '{}.{}'.format(self.CT_OBJ_LINE, line.id)
    
    def ct_hexagon_tag(self, hexagon):
        return '{}.{}'.format(self.CT_OBJ_HEXAGON, hexagon.id)

    def ct_node_tag(self, node):
        return '{}.{}'.format(self.CT_OBJ_NODE, node.id)