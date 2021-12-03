from backend.mechanics.Distributor import Distributor
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
        self.render_robber(self.UNFOCUSED)
        self.border_render.thicken_coastlines()
    
    def focus(self):
        ### Overlay darker hexagon and thick border when cursor gets near
        self.set_focused(True)
        polygon_id = self.body_render.render_polygon(self.FOCUSED)
        self.body_render.render_text_elements(self.FOCUSED)
        self.render_robber(self.FOCUSED)
        return polygon_id
    
    def unfocus(self, hexagons_to_focus = []):
        ### Remove darker hexagon overlay and thick border when cursor moves away
        self.set_focused(False)
        self.rendering.delete_tag('{}.{}'.format(self.hexagon_tag, self.FOCUSED))
    
    def render_robber(self, focused):
        hexagon = self.rendering.distributor().get_object_by_id(Distributor.OBJ_HEXAGON, self.hexagon.id)
        if hexagon.robber:
            centre_point = hexagon.centre_point()
            x, y = (self.rendering.real_x(centre_point), self.rendering.real_y(centre_point))
            dist = self.rendering.scale / 4
            point_1 = (x, y - dist)
            point_2 = (x - dist, y + dist)
            point_3 = (x + dist, y + dist)
            points = (point_1, point_2, point_3)
            tags = [
                self.rendering.CT_OBJ_ROBBER,
                self.hexagon_tag,
                '{}.{}'.format(self.hexagon_tag, focused),
                self.rendering.CV_OBJ_POLYGON
            ]
            self.rendering.create_polygon(points, fill = 'black', outline = 'black', tags = tags, width = 2) ### TODO: Make transparent?