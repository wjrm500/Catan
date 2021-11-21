import abc
import tkinter

class BaseFrame:
    def __init__(self, notebook) -> None:
        self.frame = tkinter.Frame(notebook)

    def get(self):
        return self.frame
    
    @abc.abstractmethod
    def setup(self):
        pass