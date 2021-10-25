import tkinter
from GeneralUtils import GeneralUtils
from frontend.Tkinter.phases.primary.SetupPhase import SetupPhase
from frontend.ColorUtils import ColorUtils

### Lobby game code needs to be visible
### LobbyPhase can be accessed by creator and joiners, should appear differently to both. For creator, option to proceed

class LobbyPhase(SetupPhase):
    MAX_PLAYER_COUNT = 4

    def __init__(self, chaperone):
        super().__init__(chaperone)
        self.split_panel = self.render_frame(where = self.inner_frame, size = 1.0)
        player_panel_config = {
            'background': ColorUtils.lighten_hex(self.BG_COLOR, 0.1),
            'highlightbackground': ColorUtils.darken_hex(self.BG_COLOR, 0.2),
            'highlightcolor': ColorUtils.darken_hex(self.BG_COLOR, 0.2), 
            'highlightthickness': 1
        }
        self.game_code_label = self.render_label(where = self.inner_frame, text = 'Game code: {}'.format(self.chaperone.game_code))
        self.game_code_label.pack(side = tkinter.TOP, pady = 20)
        self.new_player_panel = self.render_new_player_panel(where = self.split_panel, config = player_panel_config)
        self.existing_players_panel = self.render_existing_players_panel(where = self.split_panel, config = player_panel_config)
        self.split_panel.pack(side = tkinter.TOP, pady = 20)
        self.new_player_panel.pack(side = tkinter.LEFT, fill = 'y', padx = 10)
        self.existing_players_panel.pack(side = tkinter.RIGHT, fill = 'y', padx = 10)
        self.new_player_input.focus()

    def run(self):
        self.add_new_player_button.bind('<Button-1>', self.add_player)
        self.new_player_input.bind('<Return>', self.add_player)
        self.root.mainloop()
    
    def add_player(self, event):
        name = self.new_player_input.get()
        errors = []
        players = self.chaperone.get_players()
        if len(players) == self.MAX_PLAYER_COUNT:
            errors.append('Only {} players allowed'.format(self.MAX_PLAYER_COUNT))
        name = name.title()
        if name in players:
            errors.append('The name {} is taken'.format(name))
        if len(errors) == 0:
            self.chaperone.add_player(name)
            if hasattr(self, 'existing_players_list'):
                self.existing_players_list.destroy()
            self.existing_players_list = self.render_existing_players_list(where = self.existing_players_panel, config = {'background': ColorUtils.lighten_hex(self.BG_COLOR, 0.1)})
            self.existing_players_list.pack(side = tkinter.TOP, pady = 10)
            self.new_player_input.delete(0, 'end')
        else:
            self.error_text = self.render_error_text(self.inner_frame, '\n'.join(errors))
            self.error_text.pack(side = tkinter.TOP, pady = 10)

    def render_new_player_panel(self, where, config):
        new_player_panel = self.render_frame(where = where, size = 1.0, config = config)
        player_name_label = self.render_label(where = new_player_panel, text = 'Please enter your name:', config = GeneralUtils.filter_dict(config, ['background']))
        self.new_player_input = self.render_input(where = new_player_panel)
        self.add_new_player_button = self.render_button(where = new_player_panel, text = 'Submit')
        panel_components = [player_name_label, self.new_player_input, self.add_new_player_button]
        for component in panel_components:
            component.pack(side = tkinter.TOP, pady = 20)
        return new_player_panel
        
    def render_existing_players_panel(self, where, config):
        existing_players_panel = self.render_frame(where = where, size = 1.0, config = config)
        existing_players_label = self.render_label(where = existing_players_panel, text = 'Players in lobby:', config = GeneralUtils.filter_dict(config, ['background']))
        self.existing_players_list = self.render_existing_players_list(where = existing_players_panel, config = GeneralUtils.filter_dict(config, ['background']))
        existing_players_label.pack(side = tkinter.TOP, pady = 20)
        self.existing_players_list.pack(side = tkinter.TOP, pady = 20)
        return existing_players_panel
    
    def render_existing_players_list(self, where, config):
        players = self.chaperone.get_players()
        existing_players_list = tkinter.Text(where, font = self.get_font(font_weight = 'normal'), foreground = 'black', background = self.BG_COLOR, width = 25, height = len(players) + 1, bd = 0)
        existing_players_list.config(config)
        existing_players_list.tag_configure('tag-center', justify = 'center')
        for player in players:
            existing_players_list.insert(tkinter.END, '{}\n'.format(player), 'tag-center')
        return existing_players_list

    def go_to_main_loop(self, event):
        self.chaperone.start_main_phase()