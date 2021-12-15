import tkinter
from actions.Action import Action
from frontend.Tkinter.phases.game.sub_phases.MainGamePhase import MainGamePhase

class StartGameProper(Action):
    def __init__(self):
        pass

    def callback(self, chaperone, data):
        self.chaperone = chaperone
        self.game_phase = self.chaperone.current_phase
        chaperone.root.after(100, chaperone.check_queue) ### Whenever starting new phase in callback, need to call this, otherwise queue no longer checked
        chaperone.root.unbind('<Configure>')
        chaperone.settling_phase_text = chaperone.current_phase.text_area.get('1.0', tkinter.END) ### Store so we can grab in main game phase and dump in history frame
        chaperone.start_phase(MainGamePhase)
        self.refresh_status_frame_handler()