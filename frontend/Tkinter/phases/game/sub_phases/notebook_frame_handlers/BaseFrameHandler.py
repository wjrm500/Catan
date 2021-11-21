import abc
import tkinter

class BaseFrameHandler:
    def __init__(self, root, notebook) -> None:
        self.root = root
        self.frame = tkinter.Frame(notebook)

    def get(self):
        return self.frame
    
    @abc.abstractmethod
    def setup(self):
        pass