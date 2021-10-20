import tkinter
from frontend.Tkinter.phases.primary.SetupPhase import SetupPhase
from frontend.ColorUtils import ColorUtils

class LobbyPhase(SetupPhase):
    MAX_PLAYER_COUNT = 2

    def __init__(self, chaperone):
        super().__init__(chaperone)
        self.player_name_label = self.render_label(where = self.inner_frame, text = 'Please enter your name:')
        self.player_name_input = self.render_input(where = self.inner_frame)
        self.submit_button = self.render_submit_button(where = self.inner_frame)
        inner_frame_components = [self.player_name_label, self.player_name_input, self.submit_button]
        for component in inner_frame_components:
            component.pack(side = tkinter.TOP, pady = 20)
        self.player_name_input.focus()

    def run(self):
        self.submit_button.bind('<Button-1>', self.add_name)
        self.player_name_input.bind('<Return>', self.add_name)
        self.root.mainloop()
    
    def add_name(self, event):
        name = self.player_name_input.get()
        errors = []
        if len(self.chaperone.player_names) == self.MAX_PLAYER_COUNT:
            errors.append('Only {} players allowed'.format(self.MAX_PLAYER_COUNT))
        if name in self.chaperone.player_names:
            errors.append('The name {} is taken'.format(name))
        if len(errors) == 0:
            self.chaperone.player_names.append(name)
            if hasattr(self, 'player_name_list'):
                self.player_name_list.destroy()
            self.player_name_list = self.render_player_name_list(self.inner_frame)
            self.player_name_list.pack(side = tkinter.TOP, pady = 10)
        else:
            self.error_text = self.render_error_text(self.inner_frame, '\n'.join(errors))
            self.error_text.pack(side = tkinter.TOP, pady = 10)
    
    def render_player_name_list(self, where):
        player_names = self.chaperone.player_names
        player_name_list = tkinter.Text(self.inner_frame, font = self.get_font(), foreground = 'black', background = self.BG_COLOR, width = 25, height = len(player_names) + 1, bd = 0)
        player_name_list.tag_configure('tag-center', justify = 'center')
        player_name_list.insert(tkinter.END, 'Players in lobby:\n', 'tag-center')
        for player_name in player_names:
            player_name_list.insert(tkinter.END, '{}\n'.format(player_name), 'tag-center')
        return player_name_list
    
    def go_to_main_loop(self, event):
        self.chaperone.start_main_phase()