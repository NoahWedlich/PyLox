from enum import Enum
from typing import Union
from errors import ErrorPos

class AutoNumber(Enum):
    def __new__(cls):
        value = len(cls.__members__)
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

class TokenType(AutoNumber):
    LEFT_PAREN = ()
    RIGHT_PAREN = ()
    LEFT_BRACE = ()
    RIGHT_BRACE = ()
    COMMA = ()
    DOT = ()
    MINUS = ()
    PLUS = ()
    SEMICOLON = ()
    SLASH = ()
    STAR = ()
    QUERY = ()
    COLON = ()

    BANG = ()
    BANG_EQUAL = ()
    EQUAL = ()
    EQUAL_EQUAL = ()
    GREATER = ()
    GREATER_EQUAL = ()
    LESS = ()
    LESS_EQUAL = ()

    IDENTIFIER = ()
    STRING = ()
    NUMBER = ()

    AND = ()
    CLASS = ()
    ELSE = ()
    FALSE = ()
    FUN = ()
    FOR = ()
    IF = ()
    NIL = ()
    OR = ()
    PRINT = ()
    RETURN = ()
    SUPER = ()
    THIS = ()
    TRUE = ()
    VAR = ()
    WHILE = ()

    ERROR = ()
    EOF = ()

class Token:
    def __init__(self, tokenType: TokenType, lexeme: str, literal: Union[str, float, bool], line: int, char: int) -> None:
        self.tokenType: TokenType = tokenType
        self.lexeme: str = lexeme
        self.literal: str = literal
        self.pos: ErrorPos = ErrorPos(line, char, line, char + len(lexeme) - 1)

    def __str__(self) -> str:
        return f"[{self.tokenType.name}] \"{self.lexeme}\" at {self.pos}"
