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
    @abstractmethod
    def visitBlockStmt(self, stmt): pass
    @abstractmethod
    def visitIfStmt(self, stmt): pass

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

class BlockStmt(Stmt):
    def __init__(self, statements: list[Stmt]) -> None:
        self.statements: list[Stmt] = statements

    def accept(self, visitor: StmtVisitor):
        visitor.visitBlockStmt(self)

class IfStmt(Stmt):
    def __init__(self, condition: Expr, thenBranch: Stmt, elseBranch: Stmt):
        self.condition: Expr = condition
        self.thenBranch: Stmt = thenBranch
        self.elseBranch: Stmt = elseBranch

    def accept(self, visitor: StmtVisitor):
        visitor.visitIfStmt(self)