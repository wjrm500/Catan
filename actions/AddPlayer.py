from actions.Action import Action
import tkinter

from frontend.ColorUtils import ColorUtils

class AddPlayer(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        self.chaperone = chaperone
        self.data = data
        chaperone.players.append(data['player'])
        if isinstance(chaperone.player, str): ### If the receiving client was also the sending client
            chaperone.player = data['player']
        self.update_gui()
    
    def update_gui(self):
        lobby_phase = self.chaperone.current_phase
        lobby_phase.game_code_text.set('Game code: {}'.format(self.chaperone.game_code))
        if hasattr(lobby_phase, 'existing_players_list'):
            for list_item in lobby_phase.existing_players_list:
                list_item.destroy()
        lobby_phase.existing_players_list = lobby_phase.render_existing_players_list(where = lobby_phase.existing_players_panel, config = {'background': ColorUtils.lighten_hex(lobby_phase.BG_COLOR, 0.1)})
        for i, list_item in enumerate(lobby_phase.existing_players_list):
            list_item.pack(side = tkinter.TOP, pady = (10, 5) if i == 0 else (5, 5))
        if hasattr(lobby_phase, 'proceed_button'):
            lobby_phase.proceed_button.destroy()
        # if self.chaperone.main and len(self.chaperone.players) > 1:
        if self.chaperone.main and len(self.chaperone.players) > 0: ### TODO: Replace with commented line above - temporary change for testing
            lobby_phase.proceed_button = lobby_phase.render_button(where = lobby_phase.inner_frame, text = 'Start game')
            lobby_phase.proceed_button.pack(side = tkinter.TOP, pady = 10)
            lobby_phase.proceed_button.bind('<Button-1>', lobby_phase.start_game)