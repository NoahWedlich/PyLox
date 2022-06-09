from expr import ExprVisitor, Expr, Literal, Grouping, Unary, Binary, Ternary, ErrorExpr, Variable, Assignment
from stmt import StmtVisitor, Stmt, ErrorStmt, ExprStmt, PrintStmt, VarStmt
from tokens import TokenType, Token
from typing import Union
from errors import PyLoxRuntimeError, ErrorHandler
from plobject import PLObjType, PLObject
from environment import Environment

class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self, errorHandler: ErrorHandler) -> None:
        self.__errorHandler = errorHandler
        self.__environment = Environment()

    def __evaluate(self, expr: Expr) -> PLObject:
        return expr.accept(self)

    def __execute(self, stmt: Stmt) -> None:
        stmt.accept(self)

    def interpret(self, program: list[Stmt]) -> None:
        try:
            for stmt in program:
                self.__execute(stmt)
        except PyLoxRuntimeError as e:
            self.__errorHandler.runtimeError(e.pos)

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
                return PLObject(PLObjType.BOOL, not right)
            return PLObject(PLObjType.NIL, None)
        except PyLoxRuntimeError as e:
            raise PyLoxRuntimeError(expr.operator.pos, e.message)

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
            raise PyLoxRuntimeError(expr.operator.pos, e.message)

    def visitTernaryExpr(self, expr: Ternary) -> PLObject:
        if self.__evaluate(expr.left):
            return self.__evaluate(expr.mid)
        else:
            return self.__evaluate(expr.right)

    def visitVariableExpr(self, expr: Variable) -> PLObject:
        return self.__environment.get(expr.name)

    def visitAssignmentExpr(self, expr: Assignment) -> PLObject:
        value = self.__evaluate(expr.value)
        self.__environment.assign(expr.name, value)
        return value

    def visitErrorExpr(self, expr: ErrorExpr):
        return None

    def visitErrorStmt(self, stmt: ErrorStmt):
        return None

    def visitExpressionStmt(self, stmt: ExprStmt) -> None:
        self.__evaluate(stmt.expression)

    def visitPrintStmt(self, stmt: PrintStmt) -> None:
        value = self.__evaluate(stmt.expression)
        print(value)

    def visitVarStmt(self, stmt: VarStmt) -> None:
        value: PLObject = PLObject(PLObjType.NIL, None)
        if stmt.initializer != None:
            value = self.__evaluate(stmt.initializer)
        self.__environment.define(stmt.name.lexeme, value)