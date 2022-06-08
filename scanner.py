from tokens import Token, TokenType
from typing import Union, Tuple
from errors import ErrorHandler

class Scanner:
    def __init__(self, source:str, errorHandler: ErrorHandler) -> None:
        self.source: str = source
        self.tokens: list[Token] = []

        self.__start: int = 0
        self.__current: int = 0
        self.__line: int = 1
        self.__char: int = 0

        self.errorHandler = errorHandler

    def __isAtEnd(self) -> bool:
        return self.__current >= len(self.source)

    def __peek(self) -> str:
        if self.__isAtEnd(): return "\0"
        return self.source[self.__current]

    def __peekNext(self) -> str:
        if self.__current + 1 >= len(self.source): return "\0"
        return self.source[self.__current + 1]

    def __advance(self, amount: int = 1) -> str:
        for _ in range(amount):
            self.__current += 1
            self.__char += 1
        return self.source[self.__current - 1]

    def __match(self, expected: str) -> bool:
        if self.__isAtEnd(): return False
        if self.source[self.__current] != expected: return False
        self.__current += 1
        self.__char += 1
        return True

    def __newLine(self):
        self.__line += 1
        self.__char = 0


    def __error(self, message: str, offset: int = 0) -> None:
        self.errorHandler.error(self.__line, self.__char + offset, message, offset)

    def __addToken(self, tokenType: TokenType, literal: Union[str, float, bool] = "") -> None:
        lexeme = self.source[self.__start:self.__current]
        self.tokens.append(Token(tokenType, lexeme, literal, self.__line, self.__char - (len(lexeme)-1)))

    def __string(self) -> None:
        while self.__peek() != "\"" and not self.__isAtEnd():
            if self.__peek() == "\n":
                self.__newLine()
            self.__advance()
        
        if self.__isAtEnd():
            self.__error("Unterminated string")
        else:
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

    def __scanToken(self) -> None:
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
        elif currentChar == "?":
            self.__addToken(TokenType.QUERY)
        elif currentChar == ":":
            self.__addToken(TokenType.COLON)
        elif currentChar == "!":
            self.__addToken(TokenType.BANG_EQUAL if self.__match("=") else TokenType.BANG)
        elif currentChar == "=":
            self.__addToken(TokenType.EQUAL_EQUAL if self.__match("=") else TokenType.EQUAL)
        elif currentChar == "<":
            self.__addToken(TokenType.LESS_EQUAL if self.__match("=") else TokenType.LESS)
        elif currentChar == ">":
            self.__addToken(TokenType.GREATER_EQUAL if self.__match("=") else TokenType.GREATER)
        elif currentChar == "/":
            if self.__match("/"):
                while not self.__isAtEnd() and self.__peek() != "\n" : self.__advance()
            elif self.__match("*"):
                while self.__current + 1 < len(self.source) and (self.__peek() != "*" or self.__peekNext() != "/"):
                    curChar = self.__advance()
                    if curChar == "\n":
                        self.__newLine()
                if self.__peek() == "*" and self.__peekNext() == "/":
                    self.__advance(2)
                elif self.__current + 1 >= len(self.source):
                    self.__error("Unterminated comment", 1)
            else:
                self.__addToken(TokenType.SLASH)
        elif currentChar == "\"":
            self.__string()
        elif currentChar in (" ", "\r", "\t"):
            pass
        elif currentChar == "\n":
            self.__newLine()
        else:
            if currentChar.isnumeric():
                self.__number()
            elif currentChar.isalpha() or currentChar == "_":
                self.__identifier()
            else:
                self.__error(f"Unexpected character \"{currentChar}\"")
                self.__addToken(TokenType.ERROR)

    def scanTokens(self) -> list[Token]:
        while not self.__isAtEnd():
            self.__start = self.__current
            self.__scanToken()
        
        self.__addToken(TokenType.EOF)
        return self.tokens

    def dumpTokens(self):
        for token in self.tokens:
            print(token)