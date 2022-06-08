from ctypes import py_object
from expr import Visitor, Expr, Literal, Grouping, Unary, Binary, Ternary, ErrorExpr
from tokens import TokenType, Token
from typing import Union
from errors import PyLoxRuntimeError, ErrorHandler
from plobject import PLObjType, PLObject

class Interpreter(Visitor):
    def __init__(self, errorHandler: ErrorHandler) -> None:
        self.errorHandler = errorHandler

    def __evaluate(self, expr: Expr) -> PLObject:
        return expr.accept(self)

    def interpret(self, expr: Expr) -> None:
        try:
            value = self.__evaluate(expr)
            print(value)
        except PyLoxRuntimeError as e:
            self.errorHandler.runtimeError(e)

    def __checkNumberOperand(self, operator: Token, operand: Union[str, float, bool]) -> None:
        if not isinstance(operand, float):
            raise PyLoxRuntimeError(operator, f"Operand for '{operator.lexeme}' must be a number")

    def __checkNumberOperands(self, operator: Token, left: Union[str, float, bool], right: Union[str, float, bool]) -> None:
        if not isinstance(left, float):
            if not isinstance(right, float):
                raise PyLoxRuntimeError(operator, f"Both operands of '{operator.lexeme}' must be numbers")
            else:
                raise PyLoxRuntimeError(operator, f"Left operand of '{operator.lexeme}' must be a number")
        elif not isinstance(right, float):
            raise PyLoxRuntimeError(operator, f"Right operand of '{operator.lexeme}' must be a number")

    def __checkSameOperandTypes(self, operator: Token, left: Union[str, float, bool], right: Union[str, float, bool]) -> None:
        if type(left) != type(right):
            raise PyLoxRuntimeError(operator, f"Operands of '{operator.lexeme}' must have same type")

    def visitLiteralExpr(self, expr: Literal) -> PLObject:
        return expr.value

    def visitGroupingExpr(self, expr: Grouping) -> PLObject:
        return self.__evaluate(expr.expression)

    def visitUnaryExpr(self, expr: Unary) -> PLObject:
        right = self.__evaluate(expr.right)

        try:
            if expr.operator.tokenType == TokenType.MINUS:
                return -right
            elif expr.operator.tokenType == TokenType.BANG:
                return not right
            return PLObject(PLObjType.NIL, None)
        except PyLoxRuntimeError as e:
            raise PyLoxRuntimeError(expr.operator, e.message)

    def visitBinaryExpr(self, expr: Binary) -> PLObject:
        left = self.__evaluate(expr.left)
        right = self.__evaluate(expr.right)
        try:
            if expr.operator.tokenType == TokenType.PLUS:
                return left + right
            elif expr.operator.tokenType == TokenType.MINUS:
                return left - right
            elif expr.operator.tokenType == TokenType.STAR:
                return left * right
            elif expr.operator.tokenType == TokenType.SLASH:
                return left / right
            elif expr.operator.tokenType == TokenType.LESS:
                return left < right
            elif expr.operator.tokenType == TokenType.LESS_EQUAL:
                return left <= right
            elif expr.operator.tokenType == TokenType.GREATER:
                return left > right
            elif expr.operator.tokenType == TokenType.GREATER_EQUAL:
                return left >= right
            elif expr.operator.tokenType == TokenType.EQUAL_EQUAL:
                return left == right
            elif expr.operator.tokenType == TokenType.BANG_EQUAL:
                return left != right
            elif expr.operator.tokenType == TokenType.COMMA:
                return right
            return None
        except PyLoxRuntimeError as e:
            raise PyLoxRuntimeError(expr.operator, e.message)

    def visitTernaryExpr(self, expr: Ternary) -> PLObject:
        if self.__evaluate(expr.left):
            return self.__evaluate(expr.mid)
        else:
            return self.__evaluate(expr.right)

    def visitErrorExpr(self, expr: ErrorExpr):
        return None