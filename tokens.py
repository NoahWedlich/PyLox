from enum import Enum
from typing import Union

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

    BANG = ()
    BANG_EQUAL = ()
    EQUAL = ()
    EQUAL_EQUAL = ()
    GREATER = ()
    GREATE_EQUAL = ()
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

    EOF = ()

class Token:
    tokenType: TokenType
    lexeme: str
    literal: Union[str, int]
    line: int
    char: int

    def __init__(self, tokenType: TokenType, lexeme: str, literal: Union[str, float, bool], line: int, char: int) -> None:
        self.tokenType = tokenType
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
        self.char = char

    def __str__(self) -> str:
        return f"[{self.tokenType.name}] \"{self.lexeme}\" at {self.line}:{self.char}"
