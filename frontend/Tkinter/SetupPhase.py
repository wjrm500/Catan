import tkinter
from PIL import Image, ImageTk
from .Phase import Phase
from frontend.ColorUtils import ColorUtils

class SetupPhase(Phase):
    MIN_HEXAGONS = 5
    MAX_HEXAGONS = 61
    BG_COLOR = '#ADD8E6'

    def __init__(self, chaperone):
        super().__init__(chaperone)
        self.root.geometry('500x500')
        self.root.minsize(250, 250)

        self.outer_frame = tkinter.Frame(self.root, background = self.BG_COLOR)
        self.outer_frame.pack(fill = 'both', expand = True)

        self.inner_frame = tkinter.Frame(self.outer_frame, background = self.BG_COLOR, width = 250, height = 250)
        self.inner_frame.place(in_ = self.outer_frame, anchor = tkinter.CENTER, relx = 0.5, rely = 0.5)

        canvas_width = 250
        canvas_height = 100
        canvas = tkinter.Canvas(self.inner_frame, width = canvas_width, height = canvas_height, background = self.BG_COLOR, bd = 0, highlightthickness = 0)
        canvas.pack(side = tkinter.TOP, pady = 20)
        img = Image.open('./frontend/assets/images/catan_logo.png')
        resized_image_wh = max(canvas_width, canvas_height)
        img.thumbnail((resized_image_wh, resized_image_wh), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        canvas.create_image(canvas_width / 2, canvas_height / 2, image = img, anchor = tkinter.CENTER)
        canvas.image = img ### https://web.archive.org/web/20201111190625id_/http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm

        label = 'Number of hexagons:'
        num_hexagons_label = tkinter.Text(self.inner_frame, font = self.get_font(), foreground = 'black', background = self.BG_COLOR, width = 25, height = 1, bd = 0)
        num_hexagons_label.pack(side = tkinter.TOP, pady = 10)

        ### Insert horizontally centred text
        num_hexagons_label.tag_configure('tag-center', justify = 'center')
        num_hexagons_label.insert(tkinter.END, label, 'tag-center')
        num_hexagons_input = tkinter.Entry(self.inner_frame)
        num_hexagons_input.pack(side = tkinter.TOP, pady = 10)
        
        color_utils = ColorUtils()
        button_bg_color = color_utils.darken_hex(self.BG_COLOR, 0.5)
        enter_button = tkinter.Button(self.inner_frame, text = 'SUBMIT', font = self.get_font(), foreground = 'white', background = button_bg_color, width = 10, height = 1)
        enter_button.pack(side = tkinter.TOP, pady = 10)

        num_hexagons_input.focus()
        self.num_hexagons_input = num_hexagons_input
        self.enter_button = enter_button

    def run(self):
        self.enter_button.bind('<Button-1>', self.go_to_main_loop)
        self.num_hexagons_input.bind('<Return>', self.go_to_main_loop)
        self.root.mainloop()
    
    def go_to_main_loop(self, event):
        if hasattr(self, 'error_text'):
            self.error_text.pack_forget()
        num_hexagons = self.num_hexagons_input.get()
        error = None
        if num_hexagons.isnumeric():
            num_hexagons = int(num_hexagons)
            if num_hexagons in range(self.MIN_HEXAGONS, self.MAX_HEXAGONS + 1):
                self.chaperone.start_main_phase(num_hexagons)
            else:
                error = 'Number of hexagons must be between {} and {}'.format(self.MIN_HEXAGONS, self.MAX_HEXAGONS)
        else:
            error = 'Input must be numeric'
        if error:
            self.error_text = tkinter.Text(self.inner_frame, font = self.get_font(), foreground = 'red', background = self.BG_COLOR, width = 25, height = 2, bd = 0)
            self.error_text.pack(side = tkinter.TOP, pady = 10)
            self.error_text.tag_configure('tag-center', justify = 'center')
            self.error_text.insert(tkinter.END, error, 'tag-center')