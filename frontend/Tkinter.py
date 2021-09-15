import tkinter
import numpy as np

class TkinterFrontend():
    @staticmethod
    def draw_board(game, scale = 25):
        window = tkinter.Tk()
        window.title('Catan')
        canvas_height = canvas_width = 500
        c = tkinter.Canvas(window, height = canvas_height, width = canvas_width)
        c.pack()
        

        node_x_values = [node.x for node in game.distributor.nodes]
        node_y_values = [node.y for node in game.distributor.nodes]
        print(min(node_x_values))
        print(min(node_y_values))

        ### TODO: Scale and centre board in Tkinter window

        average_node_x_position = np.mean(node_x_values) * scale
        average_node_y_position = np.mean(node_y_values) * scale
        x_shift, y_shift = -average_node_x_position, -average_node_y_position
        for hexagon in game.hexagons:
            for line in hexagon.lines:
                c.create_line(
                    line.start_node.x * scale + x_shift + (canvas_width / 2),
                    line.start_node.y * scale + y_shift + (canvas_height / 2),
                    line.end_node.x * scale + x_shift + (canvas_width / 2),
                    line.end_node.y * scale + y_shift + (canvas_height / 2)
                )
        window.mainloop()