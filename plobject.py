from __future__ import annotations
from enum import Enum
from pickle import NONE
from errors import PyLoxRuntimeError

class PLObjType(Enum):
    NIL = 0
    BOOL = 1
    NUMBER = 2
    STRING = 3

    def __str__(self):
        return self.name

class PLObject():
    def __init__(self, objType: PLObjType, value) -> None:
        self.objType: PLObjType = objType
        self.value = value

    def __str__(self) -> str:
        if self.objType == PLObjType.NIL:
            return "nil"
        elif self.objType == PLObjType.NUMBER:
            txt = str(self.value)
            if txt.endswith(".0"):
                return txt[:-2]
        elif self.objType == PLObjType.BOOL:
            return "true" if self.value else "false"
        return str(self.value)

    def __repr__(self) -> str:
        return f"{self.objType}: {str(self)}"

    def __neg__(self) -> PLObject:
        if self.objType == PLObjType.NUMBER:
            return PLObject(PLObjType.NUMBER, -self.value)
        else:
            raise PyLoxRuntimeError(None, f"Bad type for negation: '{self.objType}'")

    def __bool__(self):
        return bool(self.value)

    def __add__(self, other: PLObject) -> PLObject:
        if self.objType == PLObjType.NUMBER and other.objType == PLObjType.NUMBER:
            return PLObject(PLObjType.NUMBER, self.value + other.value)
        elif self.objType == PLObjType.STRING and other.objType == PLObjType.STRING:
            return PLObject(PLObjType.STRING, self.value + other.value)
        else:
            raise PyLoxRuntimeError(None, f"Bad types for addition: '{self.objType}' and '{other.objType}'")

    def __sub__(self, other: PLObject) -> PLObject:
        if self.objType == PLObjType.NUMBER and other.objType == PLObjType.NUMBER:
            return PLObject(PLObjType.NUMBER, self.value - other.value)
        else:
            raise PyLoxRuntimeError(None, f"Bad types for subtraction: '{self.objType}' and '{other.objType}'")
    
    def __mul__(self, other: PLObject) -> PLObject:
        if self.objType == PLObjType.NUMBER and other.objType == PLObjType.NUMBER:
            return PLObject(PLObjType.NUMBER, self.value * other.value)
        else:
            raise PyLoxRuntimeError(None, f"Bad types for multiplication: '{self.objType}' and '{other.objType}'")

    def __truediv__(self, other: PLObject) -> PLObject:
        if self.objType == PLObjType.NUMBER and other.objType == PLObjType.NUMBER:
            if other.value == 0:
                raise PyLoxRuntimeError(None, "Division by zero")
            else:
                return PLObject(PLObjType.NUMBER, self.value / other.value)
        else:
            raise PyLoxRuntimeError(None, f"Bad types for division: '{self.objType}' and '{other.objType}'")

    def __lt__(self, other: PLObject) -> PLObject:
        if self.objType == PLObjType.NUMBER and other.objType == PLObjType.NUMBER:
            return PLObject(PLObjType.BOOL, self.value < other.value)
        else:
            raise PyLoxRuntimeError(None, f"Bad types for less-than comparison: '{self.objType}' and '{other.objType}'")

    def __le__(self, other: PLObject) -> PLObject:
        if self.objType == PLObjType.NUMBER and other.objType == PLObjType.NUMBER:
            return PLObject(PLObjType.BOOL, self.value <= other.value)
        else:
            raise PyLoxRuntimeError(None, f"Bad types for less-equals comparison: '{self.objType}' and '{other.objType}'")

    def __gt__(self, other: PLObject) -> PLObject:
        if self.objType == PLObjType.NUMBER and other.objType == PLObjType.NUMBER:
            return PLObject(PLObjType.BOOL, self.value > other.value)
        else:
            raise PyLoxRuntimeError(None, f"Bad types for greater-than comparison: '{self.objType}' and '{other.objType}'")

    def __ge__(self, other: PLObject) -> PLObject:
        if self.objType == PLObjType.NUMBER and other.objType == PLObjType.NUMBER:
            return PLObject(PLObjType.BOOL, self.value >= other.value)
        else:
            raise PyLoxRuntimeError(None, f"Bad types for greater-equals comparison: '{self.objType}' and '{other.objType}'")

    def __eq__(self, other: PLObject) -> PLObject:
        if self.objType == other.objType:
            return PLObject(PLObjType.BOOL, self.value == other.value)
        else:
            return PLObject(PLObjType.BOOL, False)

    def __ne__(self, other: PLObject) -> PLObject:
        if self.objType == other.objType:
            return PLObject(PLObjType.BOOL, self.value != other.value)
        else:
            return PLObject(PLObjType.BOOL, True)