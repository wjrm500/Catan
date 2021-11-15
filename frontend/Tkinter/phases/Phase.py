import tkinter
from PIL import Image, ImageTk
from frontend.ColorUtils import ColorUtils

class Phase:
    BG_COLOR = '#ADD8E6'
    CATAN_LOGO_IMG_FILEPATH = './frontend/assets/images/catan_logo.png'
    CURSOR_HAND = 'hand2'
    FONT_NAME = 'Arial'
    FONT_SIZE = '10'
    FONT_WEIGHT = 'bold'

    def __init__(self, chaperone):
        self.chaperone = chaperone
        self.root = chaperone.root
    
    def get_font(self, font_name = None, font_size = None, font_weight = None):
        return (
            font_name or self.FONT_NAME,
            font_size or self.FONT_SIZE,
            font_weight or self.FONT_WEIGHT
        )

    def render_label(self, where, text, config = None):
        param_dict = {'font': self.get_font(), 'foreground': 'black', 'background': self.BG_COLOR, 'width': 25, 'height': 1, 'bd': 0}
        if isinstance(text, tkinter.StringVar):
            label = tkinter.Label(where, textvariable = text, **param_dict)
        else:
            label = tkinter.Label(where, text = text, **param_dict)
        if config is not None:
            label.config(config)
        label.configure(anchor = 'center')
        return label
    
    def render_input(self, where):
        return tkinter.Entry(where)
    
    def render_button(self, where, text):
        button_bg_color = ColorUtils.darken_hex(self.BG_COLOR, 0.5)
        return tkinter.Button(where, text = text, font = self.get_font(), foreground = 'white', background = button_bg_color, width = 15, height = 1)
    
    def render_outer_frame(self):
        outer_frame = tkinter.Frame(self.root, background = self.BG_COLOR)
        outer_frame.pack(fill = 'both', expand = True)
        return outer_frame
    
    def render_inner_frame(self, where, size):
        inner_frame_size = self.SIDE_LENGTH * size
        inner_frame = tkinter.Frame(where, background = self.BG_COLOR, width = inner_frame_size, height = inner_frame_size)
        inner_frame.place(in_ = where, anchor = tkinter.CENTER, relx = 0.5, rely = 0.5)
        return inner_frame
    
    def render_frame(self, where, size, config = None):
        self.root.update_idletasks() ### https://stackoverflow.com/questions/34373533/winfo-width-returns-1-even-after-using-pack
        frame_width = where.winfo_width() * size
        frame_height = where.winfo_height() * size
        frame = tkinter.Frame(where, background = self.BG_COLOR, width = frame_width, height = frame_height)
        if config is not None:
            frame.config(config)
        frame.place(in_ = where, anchor = tkinter.CENTER, relx = 0.5, rely = 0.5)
        return frame
    
    def render_catan_logo_canvas(self, where, width, height):
        self.root.update_idletasks() ### https://stackoverflow.com/questions/34373533/winfo-width-returns-1-even-after-using-pack
        canvas_width = where.winfo_width() * width
        canvas_height = where.winfo_height() * height
        canvas = tkinter.Canvas(where, width = canvas_width, height = canvas_height, background = self.BG_COLOR, bd = 0, highlightthickness = 0)
        img = Image.open(self.CATAN_LOGO_IMG_FILEPATH)
        resized_image_wh = max(canvas_width, canvas_height)
        img.thumbnail((resized_image_wh, resized_image_wh), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        canvas.create_image(canvas_width / 2, canvas_height / 2, image = img, anchor = tkinter.CENTER)
        canvas.image = img ### https://web.archive.org/web/20201111190625id_/http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
        return canvas
    
    def render_error_text(self, where, text):
        if hasattr(self, 'error_text'):
            self.error_text.pack_forget()
        error_text = tkinter.Text(where, font = self.get_font(), foreground = 'red', background = self.BG_COLOR, width = 50, height = 2, bd = 0)
        error_text.tag_configure('tag-center', justify = 'center')
        error_text.insert(tkinter.END, text, 'tag-center')
        return error_text