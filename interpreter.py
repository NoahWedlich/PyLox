from expr import Visitor, Expr, Literal, Grouping, Unary, Binary, Ternary, ErrorExpr
from tokens import TokenType

class Interpreter(Visitor):
    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def visitLiteralExpr(self, expr: Literal):
        return expr.value

    def visitGroupingExpr(self, expr: Grouping):
        return self.evaluate(expr.expression)

    def visitUnaryExpr(self, expr: Unary):
        right = self.evaluate(expr.right)

        if expr.operator.tokenType == TokenType.MINUS:
            return -right
        elif expr.operator.tokenType == TokenType.BANG:
            return not right
        return None

    def visitBinaryExpr(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

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
        elif expr.operator.tokenType == TokenType.GREATE_EQUAL:
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
            return self.evaluate(expr.mid)
        else:
            return self.evaluate(expr.right)

    def visitErrorExpr(self, expr: ErrorExpr):
        return None