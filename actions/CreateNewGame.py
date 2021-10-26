from actions.Action import Action
from frontend.Tkinter.phases.primary.setup.LobbyPhase import LobbyPhase

class CreateNewGame(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        chaperone.game_code = data['game_code']