import abc
import itertools

class Incrementable(abc.ABC):
    new_id = itertools.count()

    def __init__(self):
        self.id = next(Incrementable.new_id)