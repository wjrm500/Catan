import tkinter
from GeneralUtils import GeneralUtils
from frontend.Tkinter.phases.primary.SetupPhase import SetupPhase
from frontend.ColorUtils import ColorUtils

class LobbyPhase(SetupPhase):
    MAX_PLAYER_COUNT = 4

    def __init__(self, chaperone):
        super().__init__(chaperone)
        
        self.split_panel = self.render_inner_frame(where = self.inner_frame, size = 1.0)
        player_panel_config = {
            'background': ColorUtils().lighten_hex(self.BG_COLOR, 0.1),
            'highlightbackground': ColorUtils().darken_hex(self.BG_COLOR, 0.2),
            'highlightthickness': 1
        }
        self.new_player_panel = self.render_new_player_panel(where = self.split_panel, config = player_panel_config)
        self.existing_players_panel = self.render_existing_players_panel(where = self.split_panel, config = player_panel_config)
        self.split_panel.pack(side = tkinter.TOP, pady = 20)
        self.new_player_panel.pack(side = tkinter.LEFT, fill = 'y', padx = 10)
        self.existing_players_panel.pack(side = tkinter.RIGHT, fill = 'y', padx = 10)
        
        self.player_name_input.focus()

    def run(self):
        self.add_player_name_button.bind('<Button-1>', self.add_name)
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
            if hasattr(self, 'existing_players_list'):
                self.existing_players_list.destroy()
            self.existing_players_list = self.render_existing_players_list(where = self.existing_players_panel, config = {'background': ColorUtils().lighten_hex(self.BG_COLOR, 0.1)})
            self.existing_players_list.pack(side = tkinter.TOP, pady = 10)
        else:
            self.error_text = self.render_error_text(self.inner_frame, '\n'.join(errors))
            self.error_text.pack(side = tkinter.TOP, pady = 10)

    def render_new_player_panel(self, where, config):
        new_player_panel = self.render_frame(where = where, size = 1.0)
        new_player_panel.config(config)
        player_name_label = self.render_label(where = new_player_panel, text = 'Please enter your name:', config = GeneralUtils.filter_dict(config, ['background']))
        self.player_name_input = self.render_input(where = new_player_panel)
        self.add_player_name_button = self.render_submit_button(where = new_player_panel)
        panel_components = [player_name_label, self.player_name_input, self.add_player_name_button]
        for component in panel_components:
            component.pack(side = tkinter.TOP, pady = 20)
        return new_player_panel
        
    def render_existing_players_panel(self, where, config):
        existing_players_panel = self.render_frame(where = where, size = 1.0)
        existing_players_panel.config(config)
        existing_players_label = self.render_label(where = existing_players_panel, text = 'Players in lobby:', config = GeneralUtils.filter_dict(config, ['background']))
        self.existing_players_list = self.render_existing_players_list(where = existing_players_panel, config = GeneralUtils.filter_dict(config, ['background']))
        existing_players_label.pack(side = tkinter.TOP, pady = 20)
        self.existing_players_list.pack(side = tkinter.TOP, pady = 20)
        return existing_players_panel
    
    def render_existing_players_list(self, where, config):
        player_names = self.chaperone.player_names
        existing_players_list = tkinter.Text(where, font = self.get_font(font_weight = 'normal'), foreground = 'black', background = self.BG_COLOR, width = 25, height = len(player_names) + 1, bd = 0)
        existing_players_list.config(config)
        existing_players_list.tag_configure('tag-center', justify = 'center')
        for player_name in player_names:
            existing_players_list.insert(tkinter.END, '{}\n'.format(player_name), 'tag-center')
        return existing_players_list

    def go_to_main_loop(self, event):
        self.chaperone.start_main_phase()