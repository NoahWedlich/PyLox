from typing import Union
from tokens import Token
from abc import ABC, abstractmethod

class Visitor(ABC):
    @abstractmethod
    def visitBinaryExpr(self, expr): pass
    @abstractmethod
    def visitGroupingExpr(self, expr): pass
    @abstractmethod
    def visitLiteralExpr(self, expr): pass
    @abstractmethod
    def visitUnaryExpr(self, expr): pass

class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor): pass

class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
        self.left: Expr = left
        self.operator: Token = operator
        self.right: Expr = right
    
    def accept(self, visitor: Visitor):
        return visitor.visitBinaryExpr(self)

class Grouping(Expr):
    def __init__(self, expression: Expr) -> None:
        self.expression: Expr = expression
    
    def accept(self, visitor: Visitor):
        return visitor.visitGroupingExpr(self)

class Literal(Expr):
    def __init__(self, value: Union[str, float]) -> None:
        self.value: Union[str, float] = value

    def accept(self, visitor: Visitor):
        return visitor.visitLiteralExpr(self)

class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator: Token = operator
        self.right: Expr = right
    
    def accept(self, visitor: Visitor):
        return visitor.visitUnaryExpr(self)

class AstPrinter(Visitor):
    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def __parenthesize(self, name: str, exprs: list[Expr]) -> str:
        result = f"( {name} "
        for expr in exprs:
            result += f" {expr.accept(self)}"
        result += ")"
        return result

    def visitBinaryExpr(self, expr: Binary) -> str:
        return self.__parenthesize(expr.operator.lexeme, [expr.left, expr.right])

    def visitGroupingExpr(self, expr: Grouping) -> str:
        return self.__parenthesize("group", [expr.expression])

    def visitLiteralExpr(self, expr: Literal) -> str:
        if expr.value == None: return "nil"
        return str(expr.value)

    def visitUnaryExpr(self, expr: Unary) -> str:
        return self.__parenthesize(expr.operator.lexeme, [expr.right])