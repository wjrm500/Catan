from frontend.ColorUtils import ColorUtils
import tkinter
import math
from .Phase import Phase

class MainPhase(Phase):
    def __init__(self, chaperone):
        super().__init__(chaperone)
        self.root.geometry('1000x500')
        self.left_frame = tkinter.Frame(self.root)
        self.right_frame = tkinter.Frame(self.root, background = 'white')
        self.left_frame.grid(row = 0, column = 0, sticky = 'nsew')
        self.right_frame.grid(row = 0, column = 1, sticky = 'nsew')
        self.root.grid_columnconfigure(0, weight = 1, uniform = 'group1')
        self.root.grid_columnconfigure(1, weight = 1, uniform = 'group1')
        self.root.grid_rowconfigure(0, weight = 1)
        self.canvas = tkinter.Canvas(self.left_frame, background = 'lightblue')
        self.canvas.pack(expand = True)
        self.focused_hexagons = []
        self.color_utils = ColorUtils()
        self.set_colors()
    
    def set_game(self, game):
        self.game = game

    def set_colors(self):
        self.background_colors = self.set_background_colors()
        self.focused_background_colors = self.set_focused_background_colors()
        self.text_colors = self.set_text_colors()
        self.focused_text_colors = self.set_focused_text_colors()
    
    def set_background_colors(self):
        d = {}
        for resource_type, data in self.chaperone.config['resource_types'].items():
            d[resource_type] = data['color']
        return d
    
    def set_focused_background_colors(self):
        d = {}
        for resource_type, data in self.chaperone.config['resource_types'].items():
            d[resource_type] = self.color_utils.darken_hex(data['color'], 0.2)
        return d
    
    def set_text_colors(self):
        d = {}
        for resource_type, data in self.chaperone.config['resource_types'].items():
            d[resource_type] = self.color_utils.darken_hex(data['color'], 0.4)
        return d
    
    def set_focused_text_colors(self):
        d = {}
        for resource_type, data in self.chaperone.config['resource_types'].items():
            d[resource_type] = self.color_utils.darken_hex(data['color'], 0.6)
        return d
    
    def run(self):
        self.root.bind('<Configure>', self.resize)
        self.right_frame.bind('<Motion>', self.reset_transformed_hexagons)
        self.canvas.bind('<Motion>', self.transform_hexagons)
        self.root.mainloop()
    
    def draw_board(self):
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        if self.canvas_width > 11: ### Width on initial render before resize
            self.canvas.delete('all')
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
                self.draw_tk_hexagon(hexagon)

    def resize(self, event):
        self.canvas.pack(fill = "both", expand = True)
        self.focused_hexagons = []
        for hexagon in self.focused_hexagons:
            self.remove_hexagon_border(hexagon)
        self.draw_board()
    
    def reset_transformed_hexagons(self, event):
        self.focused_hexagons = []
        for hexagon in self.focused_hexagons:
            self.remove_hexagon_border(hexagon)
        self.draw_board()
    
    def transform_hexagons(self, event_origin):
        ########################
        # Reset canvas objects #
        ########################
        
        self.canvas.delete('tk_oval')

        ##########################################
        # Calculate arguments for canvas objects #
        ##########################################

        x1 = event_origin.x
        y1 = event_origin.y

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
                self.canvas.delete(self.hexagon_tag(hexagon))
                self.draw_tk_hexagon(hexagon)
                self.remove_hexagon_border(hexagon, hexagons_to_focus)
        
        self.focused_hexagons = [hexagon for hexagon in self.focused_hexagons if hexagon in hexagons_to_focus]

        for hexagon in hexagons_to_focus:
            if hexagon not in self.focused_hexagons:
                self.draw_tk_hexagon(hexagon, True)
                self.focused_hexagons.append(hexagon)

        for args in draw_tk_oval_args_list:
            self.draw_tk_oval(args['node'], args['circle_radius'], fill = args['fill'], width = args['width'])
        
        cursor = self.CURSOR_HAND if min_node_dist / self.scale < 0.2 else ''
        self.canvas.config(cursor = cursor)
            
    def draw_tk_hexagon(self, hexagon, focused = False):
        hexagon_tag = self.hexagon_tag(hexagon)
        if focused:
            self.canvas.delete(hexagon_tag)
        points = [[node.real_x, node.real_y] for node in hexagon.nodes]
        points = [item for sublist in points for item in sublist]
        fill = self.focused_background_colors[hexagon.resource_type] if focused else self.background_colors[hexagon.resource_type]
        self.canvas.create_polygon(points, fill = fill, outline = 'black', tags = ['tk_hexagon', hexagon_tag])

        ### Add text elements
        x, y = hexagon.centre_point(True)
        text_fill = self.focused_text_colors[hexagon.resource_type] if focused else self.text_colors[hexagon.resource_type]
        show_resource_type = self.scale > 50
        roll_num_offset = -(self.scale / 4) if show_resource_type else 0
        resource_type_offset = self.scale / 4 if show_resource_type and hexagon.resource_type != 'desert' else 0
        pips_offset = self.scale / 2 if show_resource_type else self.scale / 2
        font_size = round(self.scale / 3.5 if focused else self.scale / 4)
        roll_num_font_size = round(font_size * 0.75 * math.sqrt(hexagon.num_pips))
        roll_num_text = hexagon.roll_num
        self.canvas.create_text(x, y + roll_num_offset, fill = text_fill, font = 'Arial {} bold'.format(roll_num_font_size), text = roll_num_text)
        if show_resource_type:
            resource_type_text = hexagon.resource_type.upper()
            self.canvas.create_text(x, y + resource_type_offset, fill = text_fill, font = 'Arial {} bold'.format(font_size - 4), text = resource_type_text)
        pips_text = ''.join(['·' for _ in range(hexagon.num_pips)])
        self.canvas.create_text(x, y + pips_offset, fill = text_fill, font = 'Arial {} bold'.format(font_size), text = pips_text)

        if focused:
            self.add_hexagon_border(hexagon)
    
    def add_hexagon_border(self, hexagon):
        show_line_ids = False
        line_width = round(self.scale / 10)
        for line in hexagon.lines:
            line_tag = self.line_tag(line)
            self.canvas.create_line(line.start_node.real_x, line.start_node.real_y, line.end_node.real_x, line.end_node.real_y, tags = line_tag, fill = 'black', width = line_width)
            if show_line_ids:
                (x, y) = line.centre_point(True)
                circle_radius = 10
                self.canvas.create_oval(x - circle_radius, y - circle_radius, x + circle_radius, y + circle_radius, fill = 'white', width = 1)
                font_size = round(self.scale / 4)
                self.canvas.create_text(x, y, fill = 'black', font = 'Arial {} bold'.format(font_size), text = line.id)
            if line not in hexagon.focused_lines:
                hexagon.focused_lines.append(line)
        ### Filler circles to bridge gap between lines, which is especially visible with larger hexagons
        r = line_width / 2.5
        for node in hexagon.nodes:
            node_tag = self.node_tag(node)
            self.canvas.create_oval(node.real_x - r, node.real_y - r, node.real_x + r, node.real_y + r, tags = node_tag, fill = 'black', outline = '')        
    
    def remove_hexagon_border(self, hexagon, hexagons_to_focus = []):
        all_focused_lines = [line for hexagon in hexagons_to_focus for line in hexagon.lines]
        line_width = round(self.scale / 10)
        for line in hexagon.focused_lines:
            line_tag = self.line_tag(line)
            self.canvas.delete(line_tag)
            for node in line.nodes:
                node_tag = self.node_tag(node)
                self.canvas.delete(node_tag)
            if line in all_focused_lines:
                self.canvas.create_line(line.start_node.real_x, line.start_node.real_y, line.end_node.real_x, line.end_node.real_y, tags = line_tag, fill = 'black', width = line_width)
                r = line_width / 2.5
                for node in line.nodes:
                    node_tag = self.node_tag(node)
                    self.canvas.create_oval(node.real_x - r, node.real_y - r, node.real_x + r, node.real_y + r, tags = node_tag, fill = 'black', outline = '')
        hexagon.focused_lines = [line for line in hexagon.focused_lines if line in all_focused_lines]

    def draw_tk_oval(self, node, circle_radius, fill = 'white', width = 1):
        self.canvas.create_oval(node.real_x - circle_radius, node.real_y - circle_radius, node.real_x + circle_radius, node.real_y + circle_radius, tags = 'tk_oval', fill = fill, width = width)
    
    def hexagon_tag(self, hexagon):
        return 'tk_hexagon_' + str(hexagon.id)

    def line_tag(self, line):
        return 'tk_line_' + str(line.id)

    def node_tag(self, node):
        return 'tk_node_' + str(node.id)