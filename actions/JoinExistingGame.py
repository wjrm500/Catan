from actions.Action import Action
from frontend.Tkinter.phases.primary.setup.LobbyPhase import LobbyPhase

class JoinExistingGame(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        if 'error' in data:
            chaperone.display_error_text(data['error'])
            return
        chaperone.game_code = data['game_code']
        chaperone.players = data['players']
        chaperone.start_phase(LobbyPhase)