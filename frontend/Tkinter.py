from catan.mechanics.drawing.ColorUtils import ColorUtils
import tkinter
import math
from types import SimpleNamespace

class TkinterFrontend():
    def __init__(self, game):
        self.game = game
        self.root = tkinter.Tk()
        self.root.title('Catan')
        initial_canvas_width = initial_canvas_height = 500
        self.canvas = tkinter.Canvas(
            self.root,
            width = initial_canvas_width,
            height = initial_canvas_height
        )
        self.canvas.pack(fill = "both", expand = True)
        self.tk_hexagons = [] ### Tkinter polygon objects from create_polygon
        self.tk_ovals = [] ### Tkinter oval objects from create_oval
        self.focused_hexagons = []
    
    def run(self):
        self.root.bind('<Configure>', self.resize)
        self.root.bind('<Motion>', self.node_bubbles)
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
            print('Canvas width and height is: ' + str(self.canvas_width) + ' ' + str(self.canvas_height))
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
            
            self.node_bubbles(SimpleNamespace(x = 350, y = 200))
            self.node_bubbles(SimpleNamespace(x = 300, y = 225))

    def resize(self, event):
        self.canvas.pack(fill = "both", expand = True)
        self.draw_board()
    
    def node_bubbles(self, event_origin):
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
                # a = 1
                hexagons_to_focus = [hexagon for hexagon in node.hexagons]
            if reversed_dist > 0:
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
        
        cursor = 'hand2' if min_node_dist / self.scale < 0.2 else ''
        self.canvas.config(cursor = cursor)
            
    def draw_tk_hexagon(self, hexagon, focused = False):
        hexagon_tag = self.hexagon_tag(hexagon)
        if focused:
            self.canvas.delete(hexagon_tag)
        points = [[node.real_x, node.real_y] for node in hexagon.nodes]
        points = [item for sublist in points for item in sublist]
        hex_fill_color = self.game.config['resource_types'][hexagon.resource_type]['color']
        if focused: ### Darken color
            color_utils = ColorUtils()
            rgb = color_utils.hex_to_rgb(hex_fill_color)
            rgb_fill_color = color_utils.darken_color(rgb, 0.2)
            hex_fill_color = color_utils.rgb_to_hex(rgb_fill_color)
        tk_hexagon = self.canvas.create_polygon(points, fill = hex_fill_color, outline = 'black', tags = ['tk_hexagon', hexagon_tag])
        x, y = hexagon.centre_point(True)
        ###TODO: Adjust font size depending on scale
        text = hexagon.id ### hexagon.roll_num
        self.canvas.create_text(x, y, fill = 'white', font = "Arial 10 bold", text = text)
        self.tk_hexagons.append(tk_hexagon)
        if focused:
            self.add_hexagon_border(hexagon)
    
    def remove_hexagon_border(self, hexagon, hexagons_to_focus):
        print('Removing hexagon border for: ' + str(hexagon.id))
        all_focused_lines = [line for hexagon in hexagons_to_focus for line in hexagon.lines]
        for line in hexagon.focused_lines:
            line_tag = self.line_tag(line)
            self.canvas.delete(line_tag)
            if line in all_focused_lines:
                self.canvas.create_line(line.start_node.real_x, line.start_node.real_y, line.end_node.real_x, line.end_node.real_y, tags = line_tag, fill = 'black', width = 5)
        hexagon.focused_lines = [line for line in hexagon.focused_lines if line in all_focused_lines]
    
    def add_hexagon_border(self, hexagon):
        show_line_ids = False
        print('Adding hexagon border for: ' + str(hexagon.id))
        for line in hexagon.lines:
            line_tag = self.line_tag(line)
            self.canvas.create_line(line.start_node.real_x, line.start_node.real_y, line.end_node.real_x, line.end_node.real_y, tags = line_tag, fill = 'black', width = 5)
            if show_line_ids:
                (x, y) = line.centre_point(True)
                circle_radius = 10
                self.canvas.create_oval(x - circle_radius, y - circle_radius, x + circle_radius, y + circle_radius, fill = 'white', width = 1)
                self.canvas.create_text(x, y, fill = 'black', font = "Arial 10 bold", text = line.id)
            if line not in hexagon.focused_lines:
                hexagon.focused_lines.append(line)

    def draw_tk_oval(self, node, circle_radius, fill = 'white', width = 1):
        tk_oval = self.canvas.create_oval(node.real_x - circle_radius, node.real_y - circle_radius, node.real_x + circle_radius, node.real_y + circle_radius, tags = 'tk_oval', fill = fill, width = width)
        self.tk_ovals.append(tk_oval)
    
    def hexagon_tag(self, hexagon):
        return 'tk_hexagon_' + str(hexagon.id)

    def line_tag(self, line):
        return 'tk_line_' + str(line.id)