from abc import ABC, abstractmethod
from expr import Expr
from tokens import Token, TokenType

class StmtVisitor(ABC):
    @abstractmethod
    def visitErrorStmt(self, stmt): pass
    @abstractmethod
    def visitExpressionStmt(self, stmt): pass
    @abstractmethod
    def visitPrintStmt(self, stmt): pass
    @abstractmethod
    def visitVarStmt(self, stmt): pass

class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor: StmtVisitor): pass

class ErrorStmt(Stmt):
    def accept(self, visitor: StmtVisitor):
        visitor.visitErrorStmt(self)

class ExprStmt(Stmt):
    def __init__(self, expr: Expr) -> None:
        self.expression: Expr = expr
    
    def accept(self, visitor: StmtVisitor):
        visitor.visitExpressionStmt(self)

class PrintStmt(Stmt):
    def __init__(self, expr: Expr) -> None:
        self.expression: Expr = expr

    def accept(self, visitor: StmtVisitor):
        visitor.visitPrintStmt(self)

class VarStmt(Stmt):
    def __init__(self, name: Token, initializer: Expr) -> None:
        self.name: Token = name
        self.initializer: Expr = initializer

    def accept(self, visitor: StmtVisitor):
        visitor.visitVarStmt(self)