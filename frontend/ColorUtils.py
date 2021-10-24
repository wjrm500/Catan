from colorsys import rgb_to_hls, hls_to_rgb
from PIL import ImageColor

class ColorUtils:
    def __init__(self):
        pass

    def lighten_hex(self, hex, factor):
        rgb = self.hex_to_rgb(hex)
        lightened_rgb = self.lighten_color(rgb, factor)
        return self.rgb_to_hex(lightened_rgb)

    def darken_hex(self, hex, factor):
        rgb = self.hex_to_rgb(hex)
        darkened_rgb = self.darken_color(rgb, factor)
        return self.rgb_to_hex(darkened_rgb)
    
    def hex_to_rgb(self, hex):
        return ImageColor.getcolor(hex, "RGB")
    
    def rgb_to_hex(self, rgb):
        return "#%02x%02x%02x" % rgb   

    def adjust_color_lightness(self, rgb, factor):
        (r, g, b) = rgb
        h, l, s = rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
        l = max(min(l * factor, 1.0), 0.0)
        r, g, b = hls_to_rgb(h, l, s)
        return (int(r * 255), int(g * 255), int(b * 255))
    
    def lighten_color(self, rgb, factor = 0.1):
        return self.adjust_color_lightness(rgb, 1 + factor)
    
    def darken_color(self, rgb, factor = 0.1):
        return self.adjust_color_lightness(rgb, 1 - factor)