from abc import ABC, abstractmethod
from expr import Expr

class StmtVisitor(ABC):
    @abstractmethod
    def visitExpressionStmt(self, stmt): pass
    @abstractmethod
    def visitPrintStmt(self, stmt): pass

class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor: StmtVisitor): pass

class ExprStmt(Stmt):
    def __init__(self, expr: Expr) -> None:
        self.expression = expr
    
    def accept(self, visitor: StmtVisitor):
        visitor.visitExpressionStmt(self)

class PrintStmt(Stmt):
    def __init__(self, expr: Expr) -> None:
        self.expression = expr

    def accept(self, visitor: StmtVisitor):
        visitor.visitPrintStmt(self)