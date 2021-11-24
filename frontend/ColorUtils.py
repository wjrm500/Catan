from collections import namedtuple
from colorsys import rgb_to_hls, hls_to_rgb, hsv_to_rgb, rgb_to_hsv
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
        
    @classmethod
    def get_luminance(cls, hex):
        rgb = cls.hex_to_rgb(hex)
        rgb = namedtuple('RGB', ['r', 'g', 'b'])(*rgb)
        return 0.2126 * rgb.r + 0.7152 * rgb.g + 0.0722 * rgb.b
    
    @classmethod
    def get_fg_from_bg(cls, hex, light_fg = None, dark_fg = None):
        luminance = cls.get_luminance(hex)
        return dark_fg or '#000000' if luminance > (255 / 2) else light_fg or '#FFFFFF'
    
    @classmethod
    def desaturate_hex(cls, hex, factor):
        rgb = cls.hex_to_rgb(hex)
        normalised_rgb = tuple(map(lambda x: x / 256, rgb))
        hsv = rgb_to_hsv(*normalised_rgb)
        desaturated_hsv = (hsv[0], hsv[1] * (1 - factor), hsv[2])
        desaturated_rgb = hsv_to_rgb(*desaturated_hsv)
        denormalised_rgb = tuple(map(lambda x: int(x * 256), desaturated_rgb))
        return cls.rgb_to_hex(denormalised_rgb)