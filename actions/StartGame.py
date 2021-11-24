from actions.Action import Action
from frontend.Tkinter.phases.game.sub_phases.MainGamePhase import MainGamePhase
from frontend.Tkinter.phases.game.sub_phases.SettlingPhase import SettlingPhase

class StartGame(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        chaperone.distributor = data['distributor']
        chaperone.update_players(data['players'])
        chaperone.root.after(100, chaperone.check_queue) ### Whenever starting new phase in callback, need to call this, otherwise queue no longer checked
        # chaperone.start_phase(MainGamePhase) ### TODO: Delete and replace with line below
        chaperone.start_phase(SettlingPhase)