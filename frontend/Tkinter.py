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
    
    def run(self):
        # self.draw_board()
        self.root.bind('<Configure>', self.resize)
        self.root.bind('<Button-1>', self.colour_hexagon)
        self.root.mainloop()
    
    def draw_board(self):
        self.canvas.delete('all')
        node_x_values = [node.x for node in self.game.distributor.nodes]
        node_y_values = [node.y for node in self.game.distributor.nodes]
        x_shift = -min(node_x_values)
        y_shift = -min(node_y_values)
        x_max = max(node_x_values) + x_shift
        y_max = max(node_y_values) + y_shift
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        canvas_x_max_ratio = canvas_width / x_max
        canvas_y_max_ratio = canvas_height / y_max
        scale = min(canvas_x_max_ratio, canvas_y_max_ratio) * 0.95
        x_centre_shift = (canvas_width - x_max * scale) / 2
        y_centre_shift = (canvas_height - y_max * scale) / 2
        self.centre_points = []
        # for hexagon in self.game.hexagons:
        #     for line in hexagon.lines:
        #         start_node = line.start_node
        #         end_node = line.end_node
        #         start_node.real_x = (start_node.x + x_shift) * scale + x_centre_shift
        #         start_node.real_y = (start_node.y + y_shift) * scale + y_centre_shift
        #         x_end_point = (end_node.x + x_shift) * scale + x_centre_shift
        #         y_end_point = (end_node.y + y_shift) * scale + y_centre_shift
        #         hexagon_selected = any(hexagon.selected for hexagon in line.hexagons)
        #         self.canvas.create_line(
        #             start_node.real_x, start_node.real_y , x_end_point, y_end_point, fill = 'red' if hexagon_selected else 'black'
        #         )
            # nodes = hexagon.nodes + [hexagon.nodes[0]]
            # for i, node in enumerate(hexagon.nodes):
            #     start_node = node
            #     end_node = nodes[i + 1]
            #     node.real_x = (start_node.x + x_shift) * scale + x_centre_shift
            #     node.real_y = (start_node.y + y_shift) * scale + y_centre_shift
            #     x_end_point = (end_node.x + x_shift) * scale + x_centre_shift
            #     y_end_point = (end_node.y + y_shift) * scale + y_centre_shift
            #     self.canvas.create_line(
            #         node.real_x, node.real_y, x_end_point, y_end_point, fill = 'red' if hexagon.selected else 'black'
            #     )
            # self.centre_points.append(hexagon.centre_point(True))
        
        for line in self.game.distributor.lines:
            start_node = line.start_node
            end_node = line.end_node
            start_node.real_x = (start_node.x + x_shift) * scale + x_centre_shift
            start_node.real_y = (start_node.y + y_shift) * scale + y_centre_shift
            x_end_point = (end_node.x + x_shift) * scale + x_centre_shift
            y_end_point = (end_node.y + y_shift) * scale + y_centre_shift
            hexagon_selected = any(hexagon.selected for hexagon in line.hexagons)
            self.canvas.create_line(
                start_node.real_x, start_node.real_y, x_end_point, y_end_point, fill = 'red' if hexagon_selected else 'black'
            )
        for hexagon in self.game.hexagons:
            self.centre_points.append(hexagon.centre_point(True))

    def resize(self, event):
        self.canvas.pack(fill = "both", expand = True)
        self.draw_board()
    
    def colour_hexagon(self, event_origin):
        x1 = event_origin.x
        y1 = event_origin.y
        centre_point_dists = [math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2)) for x2, y2 in self.centre_points]
        min_centre_point_dist = min(centre_point_dists)
        min_index = centre_point_dists.index(min_centre_point_dist)
        hexagon_to_colour = self.game.hexagons[min_index]
        for hexagon in self.game.hexagons:
            hexagon.selected = False
        hexagon_to_colour.selected = True
        self.draw_board()