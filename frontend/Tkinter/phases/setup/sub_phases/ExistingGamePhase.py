import tkinter
from frontend.Tkinter.phases.setup.SetupPhase import SetupPhase

class ExistingGamePhase(SetupPhase):
    def __init__(self, chaperone):
        super().__init__(chaperone)
        self.game_code_label = self.render_label(where = self.inner_frame, text = 'Game code:')
        self.game_code_input = self.render_input(where = self.inner_frame)
        self.submit_button = self.render_button(where = self.inner_frame, text = 'Submit')
        inner_frame_components = [self.game_code_label, self.game_code_input, self.submit_button]
        for component in inner_frame_components:
            component.pack(side = tkinter.TOP, pady = 20)
        self.game_code_input.focus()

    def run(self):
        self.submit_button.bind('<Button-1>', self.submit_form)
        self.game_code_input.bind('<Return>', self.submit_form)
        self.root.mainloop()
    
    def submit_form(self, event):
        game_code = self.game_code_input.get()
        self.chaperone.join_existing_game(game_code)
    
    def display_error_text(self, error_text):
        if hasattr(self, 'error_text'):
            self.error_text.destroy()
        self.error_text = self.render_error_text(self.inner_frame, error_text)
        self.error_text.pack(side = tkinter.TOP, pady = 10)