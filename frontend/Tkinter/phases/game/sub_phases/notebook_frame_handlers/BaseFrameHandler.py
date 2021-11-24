import abc
import tkinter

class BaseFrameHandler:
    def __init__(self, phase, notebook) -> None:
        self.phase = phase
        self.root = self.phase.root
        self.player = self.phase.chaperone.player
        self.frame = tkinter.Frame(notebook, background = self.phase.BG_COLOR)

    def get(self):
        return self.frame
    
    @abc.abstractmethod
    def setup(self):
        pass