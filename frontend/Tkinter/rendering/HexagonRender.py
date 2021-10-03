from frontend.Tkinter.rendering.HexagonBorderRender import HexagonBorderRender
from frontend.Tkinter.rendering.HexagonBodyRender import HexagonBodyRender

class HexagonRender:
    FOCUSED = 'focused'
    UNFOCUSED = 'unfocused'

    def __init__(self, rendering, hexagon):
        self.rendering = rendering
        self.hexagon = hexagon
        self.hexagon_tag = self.rendering.ct_hexagon_tag(self.hexagon)
        self.focused = False
        self.body_render = HexagonBodyRender(self)
        self.border_render = HexagonBorderRender(self)

    def set_focused(self, focused):
        self.focused = focused
    
    def init_render(self):
        ### Initial render
        self.body_render.render_polygon(self.UNFOCUSED)
        self.body_render.render_text_elements(self.UNFOCUSED)
    
    def focus(self):
        ### Overlay darker hexagon and thick border when cursor gets near
        self.set_focused(True)
        self.body_render.render_polygon(self.FOCUSED)
        self.body_render.render_text_elements(self.FOCUSED)
        self.border_render.add_hexagon_border()
    
    def unfocus(self, hexagons_to_focus = []):
        ### Remove darker hexagon overlay and thick border when cursor moves away
        self.set_focused(False)
        self.rendering.delete_tag('{}.{}'.format(self.hexagon_tag, self.FOCUSED))
        self.border_render.remove_hexagon_border(hexagons_to_focus)