from errors import ErrorHandler
from expr import Expr, Grouping, Unary, Binary, Ternary, ErrorExpr
from plobject import PLObjType
from tokens import Token, TokenType

class Analyzer():
    def __init__(self, errorHandler: ErrorHandler) -> None:
        self.errorHandler = errorHandler

    def __error(self, token: Token, message: str, offset: int = 0) -> PLObjType:
        if offset < len(token.lexeme) + 1: offset = len(token.lexeme) - 1
        self.errorHandler.error(token.line, token.char, message, offset)
        return PLObjType.ERROR

    def typeCheck(self, expr: Expr) -> PLObjType:
        if expr.rType != PLObjType.UNKNOWN: return expr.rType
        elif isinstance(expr, Grouping): return self.__typeCheckGrouping(expr)
        elif isinstance(expr, Unary): return self.__typeCheckUnary(expr)
        elif isinstance(expr, Binary): return self.__typeCheckBinary(expr)
        elif isinstance(expr, Ternary): return self.__typeCheckTernary(expr)
        else: return PLObjType.ERROR

    def __typeCheckGrouping(self, expr: Grouping) -> PLObjType:
        expr.rType = self.typeCheck(expr.expression)
        return expr.rType

    def __typeCheckUnary(self, expr: Unary) -> PLObjType:
        rightType = self.typeCheck(expr.right)
        if rightType == PLObjType.ERROR:
            expr.rType = PLObjType.ERROR
        if expr.operator.tokenType == TokenType.MINUS:
            if rightType != PLObjType.NUMBER:
                expr.rType = self.__error(expr.operator, f"Bad type for negation: '{rightType}'")
            else:
                expr.rType = PLObjType.NUMBER
        elif expr.operator.tokenType == TokenType.BANG:
            expr.rType = PLObjType.BOOL
        return expr.rType


    def __typeCheckBinary(self, expr: Binary):
        leftType = self.typeCheck(expr.left)
        rightType = self.typeCheck(expr.right)
        if leftType == PLObjType.ERROR or rightType == PLObjType.ERROR:
            expr.rType = PLObjType.ERROR
        elif expr.operator.tokenType == TokenType.PLUS:
            if leftType == PLObjType.NUMBER and rightType == PLObjType.NUMBER:
                expr.rType = PLObjType.NUMBER
            elif leftType == PLObjType.STRING and rightType == PLObjType.STRING:
                expr.rType = PLObjType.STRING
            else:
                expr.rType = self.__error(expr.operator, f"Bad types for addition: '{leftType}' and '{rightType}'")
        elif expr.operator.tokenType == TokenType.MINUS:
            if leftType == PLObjType.NUMBER and rightType == PLObjType.NUMBER:
                expr.rType = PLObjType.NUMBER
            else:
                expr.rType = self.__error(expr.operator, f"Bad types for subtraction: '{leftType}' and '{rightType}'")
        elif expr.operator.tokenType == TokenType.STAR:
            if leftType == PLObjType.NUMBER and rightType == PLObjType.NUMBER:
                expr.rType = PLObjType.NUMBER
            else:
                expr.rType = self.__error(expr.operator, f"Bad types for multiplication: '{leftType}' and '{rightType}'")
        elif expr.operator.tokenType == TokenType.SLASH:
            if leftType == PLObjType.NUMBER and rightType == PLObjType.NUMBER:
                expr.rType = PLObjType.NUMBER
            else:
                expr.rType = self.__error(expr.operator, f"Bad types for division: '{leftType}' and '{rightType}'")
        elif expr.operator.tokenType == TokenType.LESS:
            if leftType == PLObjType.NUMBER and rightType == PLObjType.NUMBER:
                expr.rType = PLObjType.BOOL
            else:
                expr.rType = self.__error(expr.operator, f"Bad types for less-than comparison: '{leftType}' and '{rightType}'")
        elif expr.operator.tokenType == TokenType.LESS_EQUAL:
            if leftType == PLObjType.NUMBER and rightType == PLObjType.NUMBER:
                expr.rType = PLObjType.BOOL
            else:
                expr.rType = self.__error(expr.operator, f"Bad types for less-equals comparison: '{leftType}' and '{rightType}'")
        elif expr.operator.tokenType == TokenType.GREATER:
            if leftType == PLObjType.NUMBER and rightType == PLObjType.NUMBER:
                expr.rType = PLObjType.BOOL
            else:
                expr.rType = self.__error(expr.operator, f"Bad types for greater-than comparison: '{leftType}' and '{rightType}'")
        elif expr.operator.tokenType == TokenType.GREATER_EQUAL:
            if leftType == PLObjType.NUMBER and rightType == PLObjType.NUMBER:
                expr.rType = PLObjType.BOOL
            else:
                expr.rType = self.__error(expr.operator, f"Bad types for greater-equals comparison: '{leftType}' and '{rightType}'")
        elif expr.operator.tokenType == TokenType.EQUAL_EQUAL:
            expr.rType = PLObjType.BOOL
        elif expr.operator.tokenType == TokenType.BANG_EQUAL:
            expr.rType = PLObjType.BOOL
        elif expr.operator.tokenType == TokenType.COMMA:
            expr.rType = rightType
        return expr.rType

    def __typeCheckTernary(self, expr: Ternary):
        condType = self.typeCheck(expr.left)
        leftType = self.typeCheck(expr.mid)
        rightType = self.typeCheck(expr.right)
        if condType == PLObjType.ERROR or leftType == PLObjType.ERROR or rightType == PLObjType.ERROR:
            expr.rType = PLObjType.ERROR
        elif expr.leftOp.tokenType == TokenType.QUERY and expr.rightOp.tokenType == TokenType.COLON:
            if leftType == rightType:
                expr.rType = leftType
            else:
                expr.rType = self.__error(expr.leftOp, f"Operands of ternary condition have different types: '{leftType}' and '{rightType}'")
        else:
            expr.rType = self.__error(expr.leftOp, f"Invalid ternary operator")
        return expr.rType