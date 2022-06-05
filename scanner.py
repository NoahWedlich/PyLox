from tokens import Token, TokenType
from typing import Union
from errors import error

class Scanner:
    def __init__(self, source:str) -> None:
        self.source: str = source
        self.tokens: list[Token] = []

        self.__start: int = 0
        self.__current: int = 0
        self.__line: int = 1

    def __isAtEnd(self) -> bool:
        return self.__current >= len(self.source)

    def __peek(self) -> str:
        if self.__isAtEnd(): return "\0"
        return self.source[self.__current]

    def __peekNext(self) -> str:
        if self.__current + 1 >= len(self.source): return "\0"
        return self.source[self.__current + 1]

    def __advance(self) -> str:
        self.__current += 1
        return self.source[self.__current - 1]

    def __match(self, expected: str) -> bool:
        if self.__isAtEnd(): return False
        if self.source[self.__current] != expected: return False
        self.__current += 1
        return True

    def __addToken(self, tokenType: TokenType, literal: Union[str, float] = "") -> None:
        lexeme = self.source[self.__start:self.__current]
        self.tokens.append(Token(tokenType, lexeme, literal, self.__line))

    def __string(self) -> bool:
        while self.__peek() != "\"" and not self.__isAtEnd():
            if self.__peek() == "\n": self.__line += 1
            self.__advance()
        
        if self.__isAtEnd():
            error(self.__line, "Unterminated string.")
            return False

        self.__advance()
        
        value = self.source[self.__start + 1 : self.__current - 1]
        self.__addToken(TokenType.STRING, value)

    def __number(self) -> None:
        while self.__peek().isnumeric(): self.__advance()

        if self.__peek() == "." and self.__peekNext().isnumeric():
            self.__advance()
            while self.__peek().isnumeric(): self.__advance()
        
        self.__addToken(TokenType.NUMBER, float(self.source[self.__start : self.__current]))

    def __keyword(self, text: str) -> TokenType:
        if text == "and": return TokenType.AND
        elif text == "class": return TokenType.CLASS
        elif text == "else": return TokenType.ELSE
        elif text == "false": return TokenType.FALSE
        elif text == "for": return TokenType.FOR
        elif text == "fun": return TokenType.FUN
        elif text == "if": return TokenType.IF
        elif text == "nil": return TokenType.NIL
        elif text == "or": return TokenType.OR
        elif text == "print": return TokenType.PRINT
        elif text == "return": return TokenType.RETURN
        elif text == "super": return TokenType.SUPER
        elif text == "this": return TokenType.THIS
        elif text == "true": return TokenType.TRUE
        elif text == "var": return TokenType.VAR
        elif text == "while": return TokenType.WHILE
        else: return TokenType.IDENTIFIER

    def __identifier(self) -> None:
        while self.__peek().isalnum() or self.__peek() == "_": self.__advance()
        text = self.source[self.__start : self.__current]
        tokenType = self.__keyword(text)
        self.__addToken(tokenType, text)

    def __scanToken(self) -> bool:
        currentChar = self.__advance()
        if currentChar == "(":
            self.__addToken(TokenType.LEFT_PAREN)
        elif currentChar == ")":
            self.__addToken(TokenType.RIGHT_PAREN)
        elif currentChar == "{":
            self.__addToken(TokenType.LEFT_BRACE)
        elif currentChar == "}":
            self.__addToken(TokenType.RIGHT_BRACE)
        elif currentChar == ",":
            self.__addToken(TokenType.COMMA)
        elif currentChar == ".":
            self.__addToken(TokenType.DOT)
        elif currentChar == "-":
            self.__addToken(TokenType.MINUS)
        elif currentChar == "+":
            self.__addToken(TokenType.PLUS)
        elif currentChar == "*":
            self.__addToken(TokenType.STAR)
        elif currentChar == ";":
            self.__addToken(TokenType.SEMICOLON)
        elif currentChar == "!":
            self.__addToken(TokenType.BANG_EQUAL if self.__match("=") else TokenType.BANG)
        elif currentChar == "=":
            self.__addToken(TokenType.EQUAL_EQUAL if self.__match("=") else TokenType.EQUAL)
        elif currentChar == "<":
            self.__addToken(TokenType.LESS_EQUAL if self.__match("=") else TokenType.LESS)
        elif currentChar == ">":
            self.__addToken(TokenType.GREATE_EQUAL if self.__match("=") else TokenType.GREATER)
        elif currentChar == "/":
            if self.__match("/"):
                while self.__peek() != "\n" and not self.__isAtEnd(): self.__advance()
            else:
                self.__addToken(TokenType.SLASH)
        elif currentChar == "\"":
            return self.__string()
        elif currentChar in (" ", "\r", "\t"):
            pass
        elif currentChar == "\n":
            self.__line += 1
        else:
            if currentChar.isnumeric():
                self.__number()
            elif currentChar.isalpha() or currentChar == "_":
                self.__identifier()
            else:
                error(self.__line, "Unexpected character.")
                return False
        return True

    def scanTokens(self) -> (list[Token], bool):
        success = True
        while not self.__isAtEnd():
            self.__start = self.__current
            if not self.__scanToken():
                success = False
        
        self.tokens.append(Token(TokenType.EOF, "", "", self.__line))
        return self.tokens, success

    def dumpTokens(self):
        for token in self.tokens:
            print(token)