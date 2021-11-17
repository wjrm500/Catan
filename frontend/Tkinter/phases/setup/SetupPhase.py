import abc
import tkinter

from frontend.Tkinter.phases.Phase import Phase

class SetupPhase(Phase, abc.ABC):
    SIDE_LENGTH = 500

    def __init__(self, chaperone):
        super().__init__(chaperone)
        self.root.geometry('{}x{}'.format(self.SIDE_LENGTH, self.SIDE_LENGTH))
        self.root.minsize(int(self.SIDE_LENGTH / 2), int(self.SIDE_LENGTH / 2))
        self.outer_frame = self.render_outer_frame()
        self.inner_frame = self.render_inner_frame(where = self.outer_frame, size = 0.5)
        self.catan_logo_canvas = self.render_catan_logo_canvas(where = self.inner_frame, width = 1.0, height = 0.5)
        self.catan_logo_canvas.pack(side = tkinter.TOP, pady = 20)