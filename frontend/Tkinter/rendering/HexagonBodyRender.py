from frontend.ColorUtils import ColorUtils
import math
from config import config

def set_colors(darken):
    d = {}
    for resource_type, data in config['resource_types'].items():
        d[resource_type] = ColorUtils.darken_hex(data['color'], darken)
    return d

BACKGROUND_COLORS = set_colors(0.0)
FOCUSED_BACKGROUND_COLORS = set_colors(0.2)
TEXT_COLORS = set_colors(0.4)
FOCUSED_TEXT_COLORS = set_colors(0.6)

class HexagonBodyRender:
    def __init__(self, render):
        self.render = render

    def render_polygon(self, focused):
        rendering = self.render.rendering
        points = [[rendering.real_x(node), rendering.real_y(node)] for node in self.render.hexagon.nodes]
        points = [item for sublist in points for item in sublist]
        if focused == self.render.FOCUSED:
            fill = FOCUSED_BACKGROUND_COLORS[self.render.hexagon.resource_type]
        else:                                                                   
            fill = BACKGROUND_COLORS[self.render.hexagon.resource_type]
        tags = [
            self.render.rendering.CT_OBJ_HEXAGON,
            self.render.hexagon_tag,
            '{}.{}'.format(self.render.hexagon_tag, focused),
            self.render.rendering.CV_OBJ_POLYGON
        ]
        line_width = round(rendering.scale / 10) if focused == self.render.FOCUSED else 1
        self.render.rendering.create_polygon(points, fill = fill, outline = 'black', tags = tags, width = line_width)

    def render_text_elements(self, focused):
        tags = [
            self.render.rendering.CT_OBJ_HEXAGON,
            self.render.hexagon_tag,
            '{}.{}'.format(self.render.hexagon_tag, focused),
            self.render.rendering.CV_OBJ_TEXT
        ]
        rendering = self.render.rendering
        centre_point = self.render.hexagon.centre_point()
        x, y = (rendering.real_x(centre_point), rendering.real_y(centre_point))
        text_fill = FOCUSED_TEXT_COLORS[self.render.hexagon.resource_type] if focused else TEXT_COLORS[self.render.hexagon.resource_type]
        show_resource_type = self.render.rendering.scale > 50
        roll_num_offset = -(self.render.rendering.scale / 4) if show_resource_type else 0
        resource_type_offset = self.render.rendering.scale / 4 if show_resource_type and self.render.hexagon.resource_type != 'desert' else 0
        pips_offset = self.render.rendering.scale / 2 if show_resource_type else self.render.rendering.scale / 2
        font_size = round(self.render.rendering.scale / 3.5 if self.render.focused else self.render.rendering.scale / 4)
        roll_num_font_size = round(font_size * 0.75 * math.sqrt(self.render.hexagon.num_pips))
        roll_num_text = self.render.hexagon.roll_num
        self.render.rendering.create_text(x, y + roll_num_offset, fill = text_fill, font = 'Arial {} bold'.format(roll_num_font_size), text = roll_num_text, tags = tags)
        if show_resource_type:
            resource_type_text = self.render.hexagon.resource_type.upper()
            self.render.rendering.create_text(x, y + resource_type_offset, fill = text_fill, font = 'Arial {} bold'.format(font_size - 4), text = resource_type_text, tags = tags)
        pips_text = ''.join(['·' for _ in range(self.render.hexagon.num_pips)])
        self.render.rendering.create_text(x, y + pips_offset, fill = text_fill, font = 'Arial {} bold'.format(font_size), text = pips_text, tags = tags)