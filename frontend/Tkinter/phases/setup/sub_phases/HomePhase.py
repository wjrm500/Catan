import tkinter
from frontend.Tkinter.phases.setup.SetupPhase import SetupPhase
from frontend.Tkinter.phases.setup.sub_phases.ExistingGamePhase import ExistingGamePhase
from frontend.Tkinter.phases.setup.sub_phases.NewGamePhase import NewGamePhase

class HomePhase(SetupPhase):
    def __init__(self, chaperone):
        super().__init__(chaperone)
        self.button_container = self.render_frame(where = self.inner_frame, size = 1.0)
        self.button_container.pack(side = tkinter.TOP, pady = 20)
        self.new_game_button = self.render_button(where = self.button_container, text = 'New game')
        self.existing_game_button = self.render_button(where = self.button_container, text = 'Existing game')
        self.new_game_button.pack(side = tkinter.LEFT, padx = 10)
        self.existing_game_button.pack(side = tkinter.RIGHT, padx = 10)

    def run(self):
        self.new_game_button.bind('<Motion>', lambda evt: self.root.configure(cursor = self.CURSOR_HAND))
        self.new_game_button.bind('<Leave>', lambda evt: self.root.configure(cursor = self.CURSOR_DEFAULT))
        self.new_game_button.bind('<Button-1>', self.create_new_game)
        self.existing_game_button.bind('<Motion>', lambda evt: self.root.configure(cursor = self.CURSOR_HAND))
        self.existing_game_button.bind('<Leave>', lambda evt: self.root.configure(cursor = self.CURSOR_DEFAULT))
        self.existing_game_button.bind('<Button-1>', self.join_existing_game)
        self.root.mainloop()
    
    def create_new_game(self, event):
        self.chaperone.start_phase(NewGamePhase)

    def join_existing_game(self, event):
        self.chaperone.start_phase(ExistingGamePhase)