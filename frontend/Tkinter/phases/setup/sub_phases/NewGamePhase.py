import tkinter
from frontend.Tkinter.phases.setup.SetupPhase import SetupPhase

class NewGamePhase(SetupPhase):
    MIN_HEXAGONS = 5
    MAX_HEXAGONS = 61

    def __init__(self, chaperone):
        super().__init__(chaperone)
        self.num_hexagons_label = self.render_label(where = self.inner_frame, text = 'Number of hexagons:')
        self.num_hexagons_input = self.render_input(where = self.inner_frame)
        self.submit_button = self.render_button(where = self.inner_frame, text = 'Submit')
        inner_frame_components = [self.num_hexagons_label, self.num_hexagons_input, self.submit_button]
        for component in inner_frame_components:
            component.pack(side = tkinter.TOP, pady = 20)
        self.num_hexagons_input.focus()

    def run(self):
        self.submit_button.bind('<Motion>', lambda evt: self.root.configure(cursor = self.CURSOR_HAND))
        self.submit_button.bind('<Leave>', lambda evt: self.root.configure(cursor = self.CURSOR_DEFAULT))
        self.submit_button.bind('<Button-1>', self.submit_form)
        self.num_hexagons_input.bind('<Return>', self.submit_form)
        self.root.mainloop()
    
    def submit_form(self, event):
        num_hexagons = self.num_hexagons_input.get()
        error = None
        if not num_hexagons.isnumeric():
            error = 'Input must be numeric'
        else:
            num_hexagons = int(num_hexagons)
            if not num_hexagons in range(self.MIN_HEXAGONS, self.MAX_HEXAGONS + 1):
                error = 'Number of hexagons must be between {} and {}'.format(self.MIN_HEXAGONS, self.MAX_HEXAGONS)
        if not error:
            self.chaperone.create_new_game(num_hexagons)
        else:
            self.error_text = self.render_error_text(self.inner_frame, error)
            self.error_text.pack(side = tkinter.TOP, pady = 10)