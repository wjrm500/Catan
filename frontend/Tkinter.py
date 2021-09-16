import tkinter

class TkinterFrontend():
    def __init__(self, game):
        self.game = game
        self.root = tkinter.Tk()
        self.root.title('Catan')
        canvas_width = canvas_height = 500
        self.canvas = tkinter.Canvas(
            self.root,
            width = canvas_width,
            height = canvas_height,
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
        scale = min(self.canvas.winfo_width() / x_max, self.canvas.winfo_height() / y_max)
        for hexagon in self.game.hexagons:
            for line in hexagon.lines:
                self.canvas.create_line(
                    (line.start_node.x + x_shift) * scale,
                    (line.start_node.y + y_shift) * scale,
                    (line.end_node.x + x_shift) * scale,
                    (line.end_node.y + y_shift) * scale
                )

    def resize(self, event):
        self.canvas.pack(fill = "both", expand = True)
        self.draw_board()
    
    def get_origin(self, event_origin):
        global x, y
        x = event_origin.x
        y = event_origin.y
        print(x,y)