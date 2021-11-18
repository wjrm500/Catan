from backend.Incrementable import Incrementable

class Port(Incrementable):
    def __init__(self, port_type):
        super().__init__()
        self.type = port_type