from tokens import Token, TokenType
from errors import ErrorHandler
from expr import Expr, Binary, Unary, Literal, Grouping, ErrorExpr
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

    def __error(self, token: Token, message: str, offset: int = 0) -> None:
        if offset < len(token.lexeme) + 1: offset = len(token.lexeme) - 1
        self.errorHandler.error(token.line, token.char, message, offset)
        # raise ParseError()

    def __consume(self, tokenType: TokenType) -> Union[Token, None]:
        if self.__check(tokenType):
            return self.__advance()
        return None

    def __checkErrorExpr(self, expr: Expr, operator: Token, message: str) -> bool:
        if isinstance(expr, ErrorExpr):
            self.__error(operator, message)
            return True
        return False

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
            openingBracket = self.__previous()
            expr = self.__expression()
            if self.__consume(TokenType.RIGHT_PAREN) == None:
                self.__error(openingBracket, "Expected closing bracket")
            return Grouping(expr)

        return ErrorExpr()

    def __unary(self) -> Expr:
        if self.__match([TokenType.BANG, TokenType.MINUS]):
            operator = self.__previous()
            right = self.__unary()
            if self.__checkErrorExpr(right, operator, f"Unary operator {operator.lexeme} expected operand"):
                return ErrorExpr()
            return Unary(operator, right)
        return self.__primary()

    def __factor(self) -> Expr:
        expr = self.__unary()
        while self.__match([TokenType.SLASH, TokenType.STAR]):
            operator = self.__previous()
            right = self.__unary()
            self.__checkErrorExpr(expr, operator, f"Binary operator {operator.lexeme} expected left operand")
            self.__checkErrorExpr(right, operator, f"Binary operator {operator.lexeme} expected right operand")
            expr = Binary(expr, operator, right)
        return expr

    def __term(self) -> Expr:
        expr = self.__factor()
        while self.__match([TokenType.MINUS, TokenType.PLUS]):
            operator = self.__previous()
            right = self.__factor()
            self.__checkErrorExpr(expr, operator, f"Binary operator {operator.lexeme} expected left operand")
            self.__checkErrorExpr(right, operator, f"Binary operator {operator.lexeme} expected right operand")
            expr = Binary(expr, operator, right)
        return expr

    def __comparison(self) -> Expr:
        expr = self.__term()
        while self.__match([TokenType.GREATER, TokenType.GREATE_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL]):
            operator = self.__previous()
            right = self.__term()
            self.__checkErrorExpr(expr, operator, f"Binary operator {operator.lexeme} expected left operand")
            self.__checkErrorExpr(right, operator, f"Binary operator {operator.lexeme} expected right operand")
            expr = Binary(expr, operator, right)
        return expr

    def __equality(self) -> Expr:
        expr = self.__comparison()
        while self.__match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]):
            operator = self.__previous()
            right = self.__comparison()
            self.__checkErrorExpr(expr, operator, f"Binary operator {operator.lexeme} expected left operand")
            self.__checkErrorExpr(right, operator, f"Binary operator {operator.lexeme} expected right operand")
            expr = Binary(expr, operator, right)
        return expr

    def __expression(self) -> Expr:
        expr = self.__equality()
        self.__checkErrorExpr(expr, Token(TokenType.EOF, "", "", 0, 0), "Expected expression")
        return self.__equality()

    def parse(self) -> Union[Expr, None]:
        try:
            return self.__expression()
        except ParseError:
            return None