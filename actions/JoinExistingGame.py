from actions.Action import Action
from frontend.Tkinter.phases.setup.sub_phases.LobbyPhase import LobbyPhase

class JoinExistingGame(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        if 'error' in data:
            chaperone.display_error_text(data['error'])
            return
        chaperone.update_players(data['players'])
        if chaperone.game_code == '': ### Only start lobby phase for new player
            chaperone.game_code = data['game_code']
            chaperone.root.after(100, chaperone.check_queue) ### Whenever starting new phase in callback, need to call this, otherwise queue no longer checked
            chaperone.start_phase(LobbyPhase)