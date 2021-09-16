import tkinter

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
        )
        self.canvas.pack(fill = "both", expand = True)
    
    def run(self):
        self.draw_board()
        self.root.bind('<Configure>', self.resize)
        self.root.bind('<Button-1>', self.get_origin)
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

        ### Centre horizontally when canvas_x_max_ratio > canvas_y_max_ratio
        ### Centre vertically when canvas_x_max_ratio < canvas_y_max_ratio

        for hexagon in self.game.hexagons:
            for line in hexagon.lines:
                x_start_point = (line.start_node.x + x_shift) * scale + x_centre_shift
                y_start_point = (line.start_node.y + y_shift) * scale + y_centre_shift
                x_end_point = (line.end_node.x + x_shift) * scale + x_centre_shift
                y_end_point = (line.end_node.y + y_shift) * scale + y_centre_shift
                self.canvas.create_line(
                    x_start_point, y_start_point, x_end_point, y_end_point
                )

    def resize(self, event):
        self.canvas.pack(fill = "both", expand = True)
        self.draw_board()
    
    def get_origin(self, event_origin):
        global x, y
        x = event_origin.x
        y = event_origin.y
        print(x,y)