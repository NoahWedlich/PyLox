from plobject import PLObject
from errors import PyLoxRuntimeError
from tokens import Token

class Environment():
    def __init__(self) -> None:
        self.__values: dict[str, PLObject] = {}

    def define(self, name: str, value: PLObject):
        self.__values[name] = value

    def get(self, name: Token) -> PLObject:
        if name.lexeme in self.__values:
            return self.__values[name.lexeme]
        else:
            raise PyLoxRuntimeError(name.pos, f"Undefined variable '{name.lexeme}'")