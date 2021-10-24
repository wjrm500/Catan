from colorsys import rgb_to_hls, hls_to_rgb
from PIL import ImageColor

class ColorUtils:
    @classmethod
    def lighten_hex(cls, hex, factor):
        rgb = cls.hex_to_rgb(hex)
        lightened_rgb = cls.lighten_color(rgb, factor)
        return cls.rgb_to_hex(lightened_rgb)

    @classmethod
    def darken_hex(cls, hex, factor):
        rgb = cls.hex_to_rgb(hex)
        darkened_rgb = cls.darken_color(rgb, factor)
        return cls.rgb_to_hex(darkened_rgb)
    
    @classmethod
    def hex_to_rgb(cls, hex):
        return ImageColor.getcolor(hex, "RGB")
    
    @classmethod
    def rgb_to_hex(cls, rgb):
        return "#%02x%02x%02x" % rgb   

    @classmethod
    def adjust_color_lightness(cls, rgb, factor):
        (r, g, b) = rgb
        h, l, s = rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
        l = max(min(l * factor, 1.0), 0.0)
        r, g, b = hls_to_rgb(h, l, s)
        return (int(r * 255), int(g * 255), int(b * 255))
    
    @classmethod
    def lighten_color(cls, rgb, factor = 0.1):
        return cls.adjust_color_lightness(rgb, 1 + factor)
    
    @classmethod
    def darken_color(cls, rgb, factor = 0.1):
        return cls.adjust_color_lightness(rgb, 1 - factor)