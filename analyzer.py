from errors import ErrorHandler
from expr import Expr, Grouping, Unary, Binary, Ternary, ErrorExpr
from plobject import PLObjType
from tokens import Token, TokenType

class Analyzer():
    def __init__(self, errorHandler: ErrorHandler) -> None:
        self.errorHandler = errorHandler

    def __error(self, token: Token, message: str, offset: int = 0) -> None:
        if offset < len(token.lexeme) + 1: offset = len(token.lexeme) - 1
        self.errorHandler.error(token.line, token.char, message, offset)
        return PLObjType.ERROR

    def typeCheck(self, expr: Expr) -> PLObjType:
        if expr.rType != PLObjType.UNKNOWN: return expr.rType
        elif isinstance(expr, Grouping): return self.__typeCheckGrouping(expr)
        elif isinstance(expr, Unary): return self.__typeCheckUnary(expr)
        elif isinstance(expr, Binary): return self.__typeCheckBinary(expr)
        elif isinstance(expr, Ternary): return self.__typeCheckTernary(expr)
        else: return

    def __typeCheckGrouping(self, expr: Grouping) -> PLObjType:
        expr.rType = self.typeCheck(expr.expression)
        return expr.rType

    def __typeCheckUnary(self, expr: Unary) -> PLObjType:
        rightType = self.typeCheck(expr.right)
        if rightType == PLObjType.ERROR:
            return PLObjType.ERROR
        if expr.operator.tokenType == TokenType.MINUS:
            if rightType != PLObjType.NUMBER:
                return self.__error(expr.operator, f"Bad type for negation: '{rightType}'")
            else:
                expr.rType = PLObjType.NUMBER
        elif expr.operator.tokenType == TokenType.BANG:
            expr.rType = PLObjType.BOOL
        return expr.rType


    def __typeCheckBinary(self, expr: Binary):
        pass

    def __typeCheckTernary(self, expr: Ternary):
        pass