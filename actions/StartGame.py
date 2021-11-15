from actions.Action import Action
from frontend.Tkinter.phases.primary.SettlingPhase import SettlingPhase

class StartGame(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        chaperone.distributor = data['distributor']
        chaperone.start_phase(SettlingPhase)