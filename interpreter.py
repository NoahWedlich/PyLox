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
            return PLObject(PLObjType.ERROR, None)
        except PyLoxRuntimeError as e:
            raise PyLoxRuntimeError(expr.operator, e.message)

    def visitTernaryExpr(self, expr: Ternary) -> PLObject:
        if self.__evaluate(expr.left):
            return self.__evaluate(expr.mid)
        else:
            return self.__evaluate(expr.right)

    def visitErrorExpr(self, expr: ErrorExpr):
        return None