import abc
import copy

class Unserializable(abc.ABC):
    @abc.abstractmethod
    def unserializable_properties(self):
        pass

    def get_serializable_copy(self):
        saved_properties = {}
        for unserializable_property in self.unserializable_properties():
            saved_properties[unserializable_property] = getattr(self, unserializable_property)
            delattr(self, unserializable_property)
        self_copy = copy.deepcopy(self)
        for key, value in saved_properties.items():
            setattr(self, key, value)
        return self_copy