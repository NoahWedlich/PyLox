from typing import Union
from tokens import Token
from abc import ABC, abstractmethod
from plobject import PLObjType, PLObject
from errors import ErrorPos

class ExprVisitor(ABC):
    @abstractmethod
    def visitBinaryExpr(self, expr): pass
    @abstractmethod
    def visitGroupingExpr(self, expr): pass
    @abstractmethod
    def visitLiteralExpr(self, expr): pass
    @abstractmethod
    def visitUnaryExpr(self, expr): pass
    @abstractmethod
    def visitErrorExpr(self, expr): pass
    @abstractmethod
    def visitTernaryExpr(self, expr): pass
    @abstractmethod
    def visitVariableExpr(self, expr): pass
    @abstractmethod
    def visitAssignmentExpr(self, expr): pass

class Expr(ABC):
    def __init__(self) -> None:
        self.pos: ErrorPos = ErrorPos(0, 0, 0, 0)
        self.rType: PLObjType = PLObjType.UNKNOWN
    @abstractmethod
    def accept(self, visitor: ExprVisitor): pass

class ErrorExpr(Expr):
    def __init__(self, pos: ErrorPos) -> None:
        self.pos: ErrorPos = pos
        self.rType: PLObjType = PLObjType.ERROR

    def accept(self, visitor: ExprVisitor):
        return visitor.visitErrorExpr(self)

class Literal(Expr):
    def __init__(self, value: PLObject, pos: ErrorPos) -> None:
        self.pos: ErrorPos = pos
        self.value: PLObject = value
        self.rType: PLObjType = value.objType

    def accept(self, visitor: ExprVisitor):
        return visitor.visitLiteralExpr(self)

class Grouping(Expr):
    def __init__(self, expression: Expr, pos: ErrorPos) -> None:
        self.pos: ErrorPos = pos
        self.expression: Expr = expression
        self.rType: PLObjType = PLObjType.UNKNOWN
    
    def accept(self, visitor: ExprVisitor):
        return visitor.visitGroupingExpr(self)

class Unary(Expr):
    def __init__(self, operator: Token, right: Expr, pos: ErrorPos):
        self.pos: ErrorPos = pos
        self.operator: Token = operator
        self.right: Expr = right
        self.rType: PLObjType = PLObjType.UNKNOWN
    
    def accept(self, visitor: ExprVisitor):
        return visitor.visitUnaryExpr(self)

class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr, pos: ErrorPos) -> None:
        self.pos: ErrorPos = pos
        self.left: Expr = left
        self.operator: Token = operator
        self.right: Expr = right
        self.rType: PLObjType = PLObjType.UNKNOWN
    
    def accept(self, visitor: ExprVisitor):
        return visitor.visitBinaryExpr(self)

class Ternary(Expr):
    def __init__(self, left: Expr, leftOp: Token, mid: Expr, rightOp: Token, right: Expr, pos: ErrorPos) -> None:
        self.pos: ErrorPos = pos
        self.left: Expr = left
        self.leftOp: Token = leftOp
        self.mid: Expr = mid
        self.rightOp: Token = rightOp
        self.right: Expr = right
        self.rType: PLObjType = PLObjType.UNKNOWN

    def accept(self, visitor: ExprVisitor):
        return visitor.visitTernaryExpr(self)

class Variable(Expr):
    def __init__(self, name: Token, pos: ErrorPos) -> None:
        self.pos: ErrorPos = pos
        self.name: Token = name
        self.rType: PLObjType = PLObjType.UNKNOWN
    
    def accept(self, visitor: ExprVisitor):
        return visitor.visitVariableExpr(self)

class Assignment(Expr):
    def __init__(self, name: Token, value: Expr, pos: ErrorPos) -> None:
        self.pos: ErrorPos = pos
        self.name: Token = name
        self.value: Expr = value
        self.rType: PLObjType = PLObjType.UNKNOWN

    def accept(self, visitor: ExprVisitor):
        return visitor.visitAssignmentExpr(self)

class AstPrinter(ExprVisitor):
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

    def visitErrorExpr(self, expr: ErrorExpr) -> str:
        return "ErrorExpr"

    def visitTernaryExpr(self, expr: Ternary) -> str:
        lO = expr.leftOp.lexeme
        rO = expr.rightOp.lexeme
        return f"({lO} {expr.left.accept(self)} ({rO} {expr.mid.accept(self)} {expr.right.accept(self)}))"

    def visitVariableExpr(self, expr: Variable) -> str:
        return f"(VAR {expr.name.lexeme}"

    def visitAssignmentExpr(self, expr: Assignment) -> str:
        return f"( = {expr.name} {expr.value.accept(self)})"