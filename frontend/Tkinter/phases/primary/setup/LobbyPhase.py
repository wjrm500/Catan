import tkinter
from frontend.Tkinter.phases.primary.SetupPhase import SetupPhase
from frontend.ColorUtils import ColorUtils

class LobbyPhase(SetupPhase):
    MAX_PLAYER_COUNT = 2

    def __init__(self, chaperone):
        super().__init__(chaperone)
        self.player_names = [] ### Game class?
        self.player_name_label = self.render_label(where = self.inner_frame, text = 'Please enter your name:')
        self.player_name_input = self.render_input(where = self.inner_frame)
        self.submit_button = self.render_submit_button(where = self.inner_frame)
        inner_frame_components = [self.player_name_label, self.player_name_input, self.submit_button]
        for component in inner_frame_components:
            component.pack(side = tkinter.TOP, pady = 20)
        self.player_name_input.focus()

    def run(self):
        self.submit_button.bind('<Button-1>', self.add_name)
        self.root.mainloop()
    
    def add_name(self, event):
        ### TODO: Prevent duplicate names
        ### TODO: Player num limit
        name = self.name_input.get()
        if len(self.player_names) == self.MAX_PLAYER_COUNT:
            return

        self.player_names.append(name)
        self.show_player_names()
    
    def show_player_names(self):
        if hasattr(self, 'player_name_list'):
            self.player_name_list.destroy()
        player_name_list = tkinter.Text(self.inner_frame, font = self.get_font(), foreground = 'black', background = self.BG_COLOR, width = 25, height = len(self.player_names) + 1, bd = 0)
        player_name_list.pack(side = tkinter.TOP, pady = 10)
        player_name_list.tag_configure('tag-center', justify = 'center')
        player_name_list.insert(tkinter.END, 'Players in lobby:\n', 'tag-center')
        for player in self.player_names:
            player_name_list.insert(tkinter.END, '{}\n'.format(player), 'tag-center')
        self.player_name_list = player_name_list
    
    def go_to_main_loop(self, event):
        self.chaperone.start_main_phase()