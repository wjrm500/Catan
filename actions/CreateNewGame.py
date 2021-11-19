from actions.Action import Action
from frontend.Tkinter.phases.setup.sub_phases.LobbyPhase import LobbyPhase

class CreateNewGame(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        chaperone.main = True
        chaperone.game_code = data['game_code']
        chaperone.root.after(100, chaperone.check_queue) ### Whenever starting new phase in callback, need to call this, otherwise queue no longer checked
        chaperone.start_phase(LobbyPhase)