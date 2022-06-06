from tokens import Token, TokenType
from errors import ErrorHandler
from expr import Expr, Binary, Unary, Literal, Grouping
from typing import Union

class ParseError(Exception):
    pass

class Parser():
    def __init__(self, tokens: list[Token], errorHandler: ErrorHandler) -> None:
        self.tokens: list[Token] = tokens
        self.__current: int = 0

        self.errorHandler = errorHandler

    def __peek(self) -> Token:
        return self.tokens[self.__current]

    def __isAtEnd(self) -> bool:
        return self.__peek().tokenType == TokenType.EOF

    def __previous(self) -> Token:
        return self.tokens[self.__current - 1]

    def __advance(self) -> Token:
        if not self.__isAtEnd(): self.__current += 1
        return self.__previous()

    def __check(self, tokenType: TokenType) -> bool:
        if self.__isAtEnd(): return False
        return self.__peek().tokenType == tokenType

    def __match(self, types: list[TokenType]):
        for tokenType in types:
            if self.__check(tokenType):
                self.__advance()
                return True
        return False

    def __error(self, token: Token, message: str) -> None:
        self.errorHandler.error(token.line, 0, message, "")
        raise ParseError()

    def __consume(self, tokenType: TokenType, msg: str) -> None:
        if self.__check(tokenType):
            return self.__advance()
        self.__error(self.__peek(), msg)

    def __synchronize(self):
        self.__advance()
        while not self.__isAtEnd():
            if self.__previous().tokenType == TokenType.SEMICOLON: return
            if self.__peek().tokenType in (
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.FOR,
                TokenType.VAR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN,
            ) : return
            self.__advance()

    def __primary(self) -> Expr:
        if self.__match([TokenType.FALSE]): return Literal(False)
        if self.__match([TokenType.TRUE]): return Literal(True)
        if self.__match([TokenType.NIL]): return Literal(None)

        if self.__match([TokenType.STRING, TokenType.NUMBER]):
            return Literal(self.__previous().literal)

        if self.__match([TokenType.LEFT_PAREN]):
            expr = self.__expression()
            self.__consume(TokenType.RIGHT_PAREN, "Expected closing bracket")
            return Grouping(expr)

        self.__error(self.__peek(), "Expected expression")

    def __unary(self) -> Expr:
        if self.__match([TokenType.BANG, TokenType.MINUS]):
            operator = self.__previous()
            right = self.__unary()
            return Unary(operator, right)
        return self.__primary()

    def __factor(self) -> Expr:
        expr = self.__unary()
        while self.__match([TokenType.SLASH, TokenType.STAR]):
            operator = self.__previous()
            right = self.__unary()
            expr = Binary(expr, operator, right)
        return expr

    def __term(self) -> Expr:
        expr = self.__factor()
        while self.__match([TokenType.MINUS, TokenType.PLUS]):
            operator = self.__previous()
            right = self.__factor()
            expr = Binary(expr, operator, right)
        return expr

    def __comparison(self) -> Expr:
        expr = self.__term()
        while self.__match([TokenType.GREATER, TokenType.GREATE_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL]):
            operator = self.__previous()
            right = self.__term()
            expr = Binary(expr, operator, right)
        return expr

    def __equality(self) -> Expr:
        expr = self.__comparison()
        while self.__match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]):
            operator = self.__previous()
            right = self.__comparison()
            expr = Binary(expr, operator, right)
        return expr
        

    def __expression(self) -> Expr:
        return self.__equality()

    def parse(self) -> Union[Expr, None]:
        try:
            return self.__expression()
        except ParseError:
            return None