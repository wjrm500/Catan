import tkinter
import math

class TkinterFrontend():
    def __init__(self, game):
        self.game = game
        self.root = tkinter.Tk()
        self.root.title('Catan')
        initial_canvas_width = initial_canvas_height = 500
        self.canvas = tkinter.Canvas(
            self.root,
            width = initial_canvas_width,
            height = initial_canvas_height,
            cursor = 'X_cursor'
        )
        self.canvas.pack(fill = "both", expand = True)
        self.tk_hexagons = [] ### Tkinter polygon objects from create_polygon
        self.tk_ovals = [] ### Tkinter oval objects from create_oval
        self.thickened_tk_hexagons = []
    
    def run(self):
        self.root.bind('<Configure>', self.resize)
        self.root.bind('<Motion>', self.node_bubbles)
        self.root.mainloop()
    
    def draw_board(self):
        self.canvas.delete('all')
        node_x_values = [node.x for node in self.game.distributor.nodes]
        node_y_values = [node.y for node in self.game.distributor.nodes]
        x_shift = -min(node_x_values)
        y_shift = -min(node_y_values)
        x_max = max(node_x_values) + x_shift
        y_max = max(node_y_values) + y_shift
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
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
        self.draw_board()
    
    def node_bubbles(self, event_origin):
        

        for hexagon in self.thickened_tk_hexagons:
            self.canvas.delete(self.hexagon_tag(hexagon))
            self.draw_tk_hexagon(hexagon)
        self.canvas.delete('tk_oval')

        x1 = event_origin.x
        y1 = event_origin.y
        node_dists = [(node, math.sqrt(pow(node.real_x - x1, 2) + pow(node.real_y - y1, 2))) for node in self.game.distributor.nodes]
        min_node_dist = min(map(lambda x: x[1], node_dists))
        for node, dist in node_dists:
            closest_to_cursor = dist == min_node_dist
            reversed_dist = max(self.scale - dist, 0)
            if closest_to_cursor:
                self.thickened_tk_hexagons = [hexagon for hexagon in node.hexagons]
                for hexagon in self.thickened_tk_hexagons:
                    self.draw_tk_hexagon(hexagon, lw_factor = reversed_dist / self.scale)
            if reversed_dist > 0:
                circle_radius = reversed_dist / 5
                fill_color = 'limegreen' if closest_to_cursor else 'white'
                tk_oval = self.canvas.create_oval(node.real_x - circle_radius, node.real_y - circle_radius, node.real_x + circle_radius, node.real_y + circle_radius, tags = 'tk_oval', fill = fill_color, width = reversed_dist / 10)
                self.tk_ovals.append(tk_oval)
            
    def draw_tk_hexagon(self, hexagon, lw_factor = 0):
        hexagon_tag = self.hexagon_tag(hexagon)
        if lw_factor:
            self.canvas.delete(hexagon_tag)
        points = [[node.real_x, node.real_y] for node in hexagon.nodes]
        points = [item for sublist in points for item in sublist]
        tk_hexagon = self.canvas.create_polygon(points, fill = '', outline = 'black', tags = ['tk_hexagon', hexagon_tag], width = 5 * lw_factor if lw_factor else 1)
        self.tk_hexagons.append(tk_hexagon)
    
    def hexagon_tag(self, hexagon):
        return 'tk_hexagon_' + str(hexagon.id)