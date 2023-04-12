from abc import ABC, abstractstaticmethod, abstractmethod

class baseModel(ABC):

    @abstractmethod
    def save(self):
        pass

    @abstractstaticmethod
    def getAll(filter):
        pass
