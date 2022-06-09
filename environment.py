from __future__ import annotations
from plobject import PLObject, PLObjType
from errors import PyLoxRuntimeError
from tokens import Token

class Environment():
    def __init__(self, enclosing: Environment = None) -> None:
        self.__enclosing: Environment = enclosing
        self.__values: dict[str, PLObject] = {}

    def define(self, name: str, value: PLObject) -> None:
        self.__values[name] = value

    def get(self, name: Token) -> PLObject:
        if name.lexeme in self.__values:
            return self.__values[name.lexeme]
        elif self.__enclosing != None:
            return self.__enclosing.get(name)
        else:
            raise PyLoxRuntimeError(name.pos, f"Undefined variable '{name.lexeme}'")

    def assign(self, name: Token, value: PLObject) -> None:
        if name.lexeme in self.__values:
            self.__values[name.lexeme] = value
        elif self.__enclosing != None:
            self.__enclosing.assign(name, value)
        else:
            raise PyLoxRuntimeError(name.pos, f"Undefined variable '{name.lexeme}'")

class TypeEnvironment():
    def __init__(self, enclosing: TypeEnvironment = None) -> None:
        self.__enclosing: TypeEnvironment = enclosing
        self.__types: dict[str, PLObjType] = {}

    def define(self, name: str, objType: PLObjType) -> None:
        self.__types[name] = objType

    def get(self, name: Token) -> PLObjType:
        if name.lexeme in self.__types:
            return self.__types[name.lexeme]
        elif self.__enclosing != None:
            return self.__enclosing.get(name)
        else:
            return PLObjType.ERROR

    def assign(self, name: Token, objType: PLObjType) -> None:
        if name.lexeme in self.__types:
            self.__types[name.lexeme] = objType
        elif self.__enclosing != None:
            self.__enclosing.assign(name, objType)
        else:
            return PLObjType.ERROR