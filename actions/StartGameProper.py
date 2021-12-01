from actions.Action import Action
from frontend.Tkinter.phases.game.sub_phases.MainGamePhase import MainGamePhase

class StartGameProper(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        chaperone.root.after(100, chaperone.check_queue) ### Whenever starting new phase in callback, need to call this, otherwise queue no longer checked
        chaperone.root.unbind('<Configure>')
        chaperone.start_phase(MainGamePhase)