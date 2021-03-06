import re
import tkinter

from frontend.ColorUtils import ColorUtils
from frontend.GeneralUtils import GeneralUtils as gutils
from frontend.Tkinter.phases.setup.SetupPhase import SetupPhase

### Lobby game code needs to be visible
### LobbyPhase can be accessed by creator and joiners, should appear differently to both. For creator, option to proceed

class LobbyPhase(SetupPhase):
    MAX_PLAYER_COUNT = 4

    def __init__(self, chaperone):
        super().__init__(chaperone)
        self.split_panel = self.render_frame(where = self.inner_frame, size = 1.0)
        player_panel_config = {
            'background': ColorUtils.lighten_hex(self.BG_COLOR, 0.1),
            'highlightbackground': self.DARKER_BG_COLOR,
            'highlightcolor': self.DARKER_BG_COLOR, 
            'highlightthickness': 1
        }
        self.ip_address_text = tkinter.StringVar()
        self.ip_address_text.set(f'IP address: {self.chaperone.get_host()}')
        self.ip_address_label = self.render_label(where = self.inner_frame, text = self.ip_address_text, config = {'background': '#eeeeee', 'font': ('Arial', '10', 'normal')})
        self.ip_address_label.pack(side = tkinter.TOP, pady = 20)
        self.new_player_panel = self.render_new_player_panel(where = self.split_panel, config = player_panel_config)
        self.existing_players_panel = self.render_existing_players_panel(where = self.split_panel, config = player_panel_config)
        self.split_panel.pack(side = tkinter.TOP, pady = 20)
        self.new_player_panel.pack(side = tkinter.LEFT, fill = 'y', padx = 10)
        self.existing_players_panel.pack(side = tkinter.RIGHT, fill = 'y', padx = 10)
        self.new_player_input.focus()

    def run(self):
        self.add_new_player_button.bind('<Motion>', lambda evt: self.root.configure(cursor = self.CURSOR_HAND))
        self.add_new_player_button.bind('<Leave>', lambda evt: self.root.configure(cursor = self.CURSOR_DEFAULT))
        self.add_new_player_button.bind('<Button-1>', self.add_player)
        self.new_player_input.bind('<Return>', self.add_player)
        self.root.mainloop()
    
    def add_player(self, event):
        if hasattr(self, 'error_text'):
            self.error_text.destroy()
        if not isinstance(self.root.focus_get(), tkinter.Entry):
            return
        new_name = self.new_player_input.get()
        errors = []
        player_names = [player.name for player in self.chaperone.players]
        if not re.match('^[A-Za-z]{1,20}$', new_name):
            errors.append(f'Invalid name: use only alphabetic characters and limit to 20 characters')
        if len(player_names) == self.MAX_PLAYER_COUNT:
            errors.append(f'Only {self.MAX_PLAYER_COUNT} players allowed')
        new_name = new_name.title()
        if new_name in player_names:
            errors.append(f'The name {new_name} is taken')
        if len(errors) == 0:
            self.chaperone.player = new_name ### Changing from None to str flags to callback that new Player object from server belongs to this client
            self.chaperone.add_player(new_name)
            ### Want the following code here and not in callback because we do not want to re-render left panel every time any other player enters name
            self.new_player_label_text.set('Name successfully submitted!')
            self.new_player_input.config(state = 'disabled')
            self.add_new_player_button.config(state = 'disabled')
            self.root.focus_set() ### Remove focus from Entry widget by setting focus to any other widget
        else:
            self.error_text = self.render_error_text(self.inner_frame, '\n'.join(errors))
            self.error_text.pack(side = tkinter.TOP, pady = 10)

    def render_new_player_panel(self, where, config):
        new_player_panel = self.render_frame(where = where, size = 1.0, config = config)
        self.new_player_label_text = tkinter.StringVar()
        self.new_player_label_text.set('Please enter your name:')
        self.new_player_label = self.render_label(where = new_player_panel, text = self.new_player_label_text, config = gutils.filter_dict(config, ['background']))
        self.new_player_input = self.render_input(where = new_player_panel)
        self.add_new_player_button = self.render_button(where = new_player_panel, text = 'Submit')
        panel_components = [self.new_player_label, self.new_player_input, self.add_new_player_button]
        for component in panel_components:
            component.pack(side = tkinter.TOP, pady = 20)
        return new_player_panel
        
    def render_existing_players_panel(self, where, config):
        existing_players_panel = self.render_frame(where = where, size = 1.0, config = config)
        existing_players_label = self.render_label(where = existing_players_panel, text = 'Players in lobby:', config = gutils.filter_dict(config, ['background']))
        self.existing_players_list = self.render_existing_players_list(where = existing_players_panel, config = gutils.filter_dict(config, ['background']))
        existing_players_label.pack(side = tkinter.TOP, pady = 20)
        for i, list_item in enumerate(self.existing_players_list):
            list_item.pack(side = tkinter.TOP, pady = (10, 5) if i == 0 else (5, 5))
        return existing_players_panel
    
    def render_existing_players_list(self, where, config):
        existing_players_list = []
        for player in self.chaperone.players:
            list_item = tkinter.Text(where, font = self.get_font(font_weight = 'normal'), foreground = 'black', background = self.BG_COLOR, width = 25, height = 1, bd = 0)
            list_item.config(config)
            list_item.tag_configure('tag-center', justify = 'center')
            you_text = ' (you)' if player is self.chaperone.player else ''
            list_item.insert(tkinter.END, f'{player.name}{you_text}', 'tag-center')
            existing_players_list.append(list_item)
        return existing_players_list

    def start_game(self, event):
        self.chaperone.start_game()