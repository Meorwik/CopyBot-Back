from abc import ABC


class Parser(ABC):
    __name__ = "Parser"

    def __repr__(self):
        return f"{self.__name__}Object - ({id(self)})"

