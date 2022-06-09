from errors import ErrorHandler, ErrorPos
from expr import Expr, Grouping, Unary, Binary, Ternary, ErrorExpr, Variable
from stmt import Stmt, ErrorStmt, ExprStmt, PrintStmt, VarStmt
from plobject import PLObjType
from tokens import Token, TokenType

class Analyzer():
    def __init__(self, errorHandler: ErrorHandler) -> None:
        self.__typeEnv: dict[str, PLObjType] = {}
        self.__errorHandler = errorHandler

    def __error(self, pos: ErrorPos, message: str) -> PLObjType:
        self.__errorHandler.error(pos, message)
        return PLObjType.ERROR

    def __typeCheckVarStmt(self, stmt: VarStmt) -> None:
        if stmt.initializer == None:
            stmt.initializer.rType = PLObjType.NIL
        else:
            stmt.initializer.rType = self.__typeCheck(stmt.initializer)
        self.__typeEnv[stmt.name.lexeme] = stmt.initializer.rType

    def typeCheckProgram(self, program: list[Stmt]) -> None:
        for stmt in program:
            if isinstance(stmt, ExprStmt) or isinstance(stmt, PrintStmt):
                self.__typeCheck(stmt.expression)
            elif isinstance(stmt, VarStmt):
                self.__typeCheckVarStmt(stmt)

    def __typeCheck(self, expr: Expr) -> PLObjType:
        if expr.rType != PLObjType.UNKNOWN: return expr.rType
        elif isinstance(expr, Grouping): return self.__typeCheckGrouping(expr)
        elif isinstance(expr, Unary): return self.__typeCheckUnary(expr)
        elif isinstance(expr, Binary): return self.__typeCheckBinary(expr)
        elif isinstance(expr, Ternary): return self.__typeCheckTernary(expr)
        elif isinstance(expr, Variable): return self.__typeCheckVariable(expr)
        else:
            self.__error(expr.pos, f"Unhandled type-check")
            return PLObjType.ERROR

    def __typeCheckGrouping(self, expr: Grouping) -> PLObjType:
        expr.rType = self.__typeCheck(expr.expression)
        return expr.rType

    def __typeCheckUnary(self, expr: Unary) -> PLObjType:
        rightType = self.__typeCheck(expr.right)
        if rightType == PLObjType.ERROR:
            expr.rType = PLObjType.ERROR
        if expr.operator.tokenType == TokenType.MINUS:
            if rightType != PLObjType.NUMBER:
                expr.rType = self.__error(expr.operator.pos, f"Bad type for negation: '{rightType}'")
            else:
                expr.rType = PLObjType.NUMBER
        elif expr.operator.tokenType == TokenType.BANG:
            expr.rType = PLObjType.BOOL
        return expr.rType


    def __typeCheckBinary(self, expr: Binary) -> PLObjType:
        leftType = self.__typeCheck(expr.left)
        rightType = self.__typeCheck(expr.right)
        if leftType == PLObjType.ERROR or rightType == PLObjType.ERROR:
            expr.rType = PLObjType.ERROR
        elif expr.operator.tokenType == TokenType.PLUS:
            if leftType == PLObjType.NUMBER and rightType == PLObjType.NUMBER:
                expr.rType = PLObjType.NUMBER
            elif leftType == PLObjType.STRING and rightType == PLObjType.STRING:
                expr.rType = PLObjType.STRING
            else:
                expr.rType = self.__error(expr.operator.pos, f"Bad types for addition: '{leftType}' and '{rightType}'")
        elif expr.operator.tokenType == TokenType.MINUS:
            if leftType == PLObjType.NUMBER and rightType == PLObjType.NUMBER:
                expr.rType = PLObjType.NUMBER
            else:
                expr.rType = self.__error(expr.operator.pos, f"Bad types for subtraction: '{leftType}' and '{rightType}'")
        elif expr.operator.tokenType == TokenType.STAR:
            if leftType == PLObjType.NUMBER and rightType == PLObjType.NUMBER:
                expr.rType = PLObjType.NUMBER
            else:
                expr.rType = self.__error(expr.operator.pos, f"Bad types for multiplication: '{leftType}' and '{rightType}'")
        elif expr.operator.tokenType == TokenType.SLASH:
            if leftType == PLObjType.NUMBER and rightType == PLObjType.NUMBER:
                expr.rType = PLObjType.NUMBER
            else:
                expr.rType = self.__error(expr.operator.pos, f"Bad types for division: '{leftType}' and '{rightType}'")
        elif expr.operator.tokenType == TokenType.LESS:
            if leftType == PLObjType.NUMBER and rightType == PLObjType.NUMBER:
                expr.rType = PLObjType.BOOL
            else:
                expr.rType = self.__error(expr.operator.pos, f"Bad types for less-than comparison: '{leftType}' and '{rightType}'")
        elif expr.operator.tokenType == TokenType.LESS_EQUAL:
            if leftType == PLObjType.NUMBER and rightType == PLObjType.NUMBER:
                expr.rType = PLObjType.BOOL
            else:
                expr.rType = self.__error(expr.operator.pos, f"Bad types for less-equals comparison: '{leftType}' and '{rightType}'")
        elif expr.operator.tokenType == TokenType.GREATER:
            if leftType == PLObjType.NUMBER and rightType == PLObjType.NUMBER:
                expr.rType = PLObjType.BOOL
            else:
                expr.rType = self.__error(expr.operator.pos, f"Bad types for greater-than comparison: '{leftType}' and '{rightType}'")
        elif expr.operator.tokenType == TokenType.GREATER_EQUAL:
            if leftType == PLObjType.NUMBER and rightType == PLObjType.NUMBER:
                expr.rType = PLObjType.BOOL
            else:
                expr.rType = self.__error(expr.operator.pos, f"Bad types for greater-equals comparison: '{leftType}' and '{rightType}'")
        elif expr.operator.tokenType == TokenType.EQUAL_EQUAL:
            expr.rType = PLObjType.BOOL
        elif expr.operator.tokenType == TokenType.BANG_EQUAL:
            expr.rType = PLObjType.BOOL
        elif expr.operator.tokenType == TokenType.COMMA:
            expr.rType = rightType
        return expr.rType

    def __typeCheckTernary(self, expr: Ternary) -> PLObjType:
        condType = self.__typeCheck(expr.left)
        leftType = self.__typeCheck(expr.mid)
        rightType = self.__typeCheck(expr.right)
        if condType == PLObjType.ERROR or leftType == PLObjType.ERROR or rightType == PLObjType.ERROR:
            expr.rType = PLObjType.ERROR
        elif expr.leftOp.tokenType == TokenType.QUERY and expr.rightOp.tokenType == TokenType.COLON:
            if leftType == rightType:
                expr.rType = leftType
            else:
                expr.rType = self.__error(expr.leftOp.pos, f"Operands of ternary condition have different types: '{leftType}' and '{rightType}'")
        else:
            expr.rType = self.__error(expr.leftOp.pos, "Invalid ternary operator")
        return expr.rType

    def __typeCheckVariable(self, expr: Variable) -> PLObjType:
        if expr.name.lexeme in self.__typeEnv:
            expr.rType = self.__typeEnv[expr.name.lexeme]
        else:
            expr.rType = self.__error(expr.pos, f"Undefined variable '{expr.name.lexeme}'")
        return expr.rType