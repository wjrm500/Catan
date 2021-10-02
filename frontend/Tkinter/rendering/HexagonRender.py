from frontend.Tkinter.rendering.HexagonBorderRender import HexagonBorderRender
from frontend.Tkinter.rendering.HexagonBodyRender import HexagonBodyRender

class HexagonRender:
    def __init__(self, rendering, hexagon):
        self.rendering = rendering
        self.hexagon = hexagon
        self.hexagon_tag = self.hexagon_tag(self.hexagon)
        self.focused = False
        self.body_render = HexagonBodyRender(self)
        self.border_render = HexagonBorderRender(self)

    def set_focused(self, focused):
        self.focused = focused
    
    def render(self):
        if self.focused:
            self.rendering.canvas.delete(self.hexagon_tag)
        self.body_render.render_polygon()
        self.body_render.render_text_elements()
        if self.focused:
            self.border_render.add_hexagon_border()
    
    def unfocus(self, hexagons_to_focus):
        self.rendering.canvas.delete(self.hexagon_tag)
        self.render()
        self.border_render.remove_hexagon_border(hexagons_to_focus)
    
    def hexagon_tag(self, hexagon):
        return 'tk_hexagon_' + str(hexagon.id)

    def line_tag(self, line):
        return 'tk_line_' + str(line.id)

    def node_tag(self, node):
        return 'tk_node_' + str(node.id)