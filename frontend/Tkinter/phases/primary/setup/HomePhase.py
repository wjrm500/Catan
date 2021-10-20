import tkinter
from frontend.Tkinter.phases.primary.SetupPhase import SetupPhase

class HomePhase(SetupPhase):
    MIN_HEXAGONS = 5
    MAX_HEXAGONS = 61

    def __init__(self, chaperone):
        super().__init__(chaperone)
        self.num_hexagons_label = self.render_label(where = self.inner_frame, text = 'Number of hexagons:')
        self.num_hexagons_input = self.render_input(where = self.inner_frame)
        self.submit_button = self.render_submit_button(where = self.inner_frame)
        inner_frame_components = [self.num_hexagons_label, self.num_hexagons_input, self.submit_button]
        for component in inner_frame_components:
            component.pack(side = tkinter.TOP, pady = 20)
        self.num_hexagons_input.focus()

    def run(self):
        self.submit_button.bind('<Button-1>', self.go_to_main_loop)
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
                self.chaperone.set_num_hexagons(num_hexagons)
                self.chaperone.start_lobby_phase()
            else:
                error = 'Number of hexagons must be between {} and {}'.format(self.MIN_HEXAGONS, self.MAX_HEXAGONS)
        else:
            error = 'Input must be numeric'
        if error:
            self.error_text = tkinter.Text(self.inner_frame, font = self.get_font(), foreground = 'red', background = self.BG_COLOR, width = 25, height = 2, bd = 0)
            self.error_text.pack(side = tkinter.TOP, pady = 10)
            self.error_text.tag_configure('tag-center', justify = 'center')
            self.error_text.insert(tkinter.END, error, 'tag-center')