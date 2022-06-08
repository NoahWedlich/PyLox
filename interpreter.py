from expr import Visitor, Expr, Literal, Grouping, Unary, Binary, Ternary, ErrorExpr
from tokens import TokenType, Token
from typing import Union
from errors import PyLoxRuntimeError, ErrorHandler

class Interpreter(Visitor):
    def __init__(self, errorHandler: ErrorHandler) -> None:
        self.errorHandler = errorHandler

    def __stringify(self, obj: Union[str, float, bool]):
        if obj == None:
            return "nil"
        elif isinstance(obj, float):
            txt = str(obj)
            if txt.endswith(".0"):
                return txt[:-2]
        return obj

    def __evaluate(self, expr: Expr):
        return expr.accept(self)

    def interpret(self, expr: Expr) -> None:
        try:
            value = self.__evaluate(expr)
            print(self.__stringify(value))
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

    def visitLiteralExpr(self, expr: Literal):
        return expr.value

    def visitGroupingExpr(self, expr: Grouping):
        return self.__evaluate(expr.expression)

    def visitUnaryExpr(self, expr: Unary):
        right = self.__evaluate(expr.right)

        if expr.operator.tokenType == TokenType.MINUS:
            self.__checkNumberOperand(expr.operator, right)
            return -right
        elif expr.operator.tokenType == TokenType.BANG:
            return not right
        return None

    def visitBinaryExpr(self, expr: Binary):
        left = self.__evaluate(expr.left)
        right = self.__evaluate(expr.right)

        if expr.operator.tokenType == TokenType.PLUS:
            self.__checkSameOperandTypes(expr.operator, left, right)
            return left + right
        elif expr.operator.tokenType == TokenType.MINUS:
            self.__checkNumberOperands(expr.operator, left, right)
            return left - right
        elif expr.operator.tokenType == TokenType.STAR:
            self.__checkNumberOperands(expr.operator, left, right)
            return left * right
        elif expr.operator.tokenType == TokenType.SLASH:
            self.__checkNumberOperands(expr.operator, left, right)
            if right == 0:
                raise PyLoxRuntimeError(expr.operator, f"Division by zero")
            return left / right
        elif expr.operator.tokenType == TokenType.LESS:
            self.__checkNumberOperands(expr.operator, left, right)
            return left < right
        elif expr.operator.tokenType == TokenType.LESS_EQUAL:
            self.__checkNumberOperands(expr.operator, left, right)
            return left <= right
        elif expr.operator.tokenType == TokenType.GREATER:
            self.__checkNumberOperands(expr.operator, left, right)
            return left > right
        elif expr.operator.tokenType == TokenType.GREATE_EQUAL:
            self.__checkNumberOperands(expr.operator, left, right)
            return left >= right
        elif expr.operator.tokenType == TokenType.EQUAL_EQUAL:
            return left == right
        elif expr.operator.tokenType == TokenType.BANG_EQUAL:
            return left != right
        elif expr.operator.tokenType == TokenType.COMMA:
            return right
        return None

    def visitTernaryExpr(self, expr: Ternary):
        if expr.left:
            return self.__evaluate(expr.mid)
        else:
            return self.__evaluate(expr.right)

    def visitErrorExpr(self, expr: ErrorExpr):
        return None