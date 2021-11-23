import abc
from copy import deepcopy

class Unserializable(abc.ABC):
    @abc.abstractmethod
    def unserializable_properties(self):
        pass
    
    def __getstate__(self):
        d = self.__dict__
        unserializable_properties = self.unserializable_properties()
        return {k: v for k, v in d.items() if k not in unserializable_properties}