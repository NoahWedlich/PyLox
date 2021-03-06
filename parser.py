from tokens import Token, TokenType
from errors import ErrorHandler, ErrorPos
from expr import Expr, Binary, Ternary, Unary, Literal, Grouping, ErrorExpr, Ternary, Variable, Assignment, Logical
from stmt import Stmt, ErrorStmt, ExprStmt, PrintStmt, VarStmt, BlockStmt, IfStmt
from typing import Union
from plobject import PLObjType, PLObject

class ParseError(Exception):
    pass

class Parser():
    def __init__(self, tokens: list[Token], errorHandler: ErrorHandler) -> None:
        self.tokens: list[Token] = tokens
        self.__current: int = 0

        self.errorHandler = errorHandler

    def __posFromTokens(self, begin: Token = None, end: Token = None) -> ErrorPos:
        if begin == None: begin = self.__previous()
        if end == None: end = self.__previous()
        return ErrorPos(begin.pos.lS, begin.pos.cS, end.pos.lE, end.pos.cE)

    def __posTokenToExpr(self, begin: Token, end: Expr) -> ErrorPos:
        return ErrorPos(begin.pos.lS, begin.pos.cS, end.pos.lE, end.pos.cE)

    def __posFromExprs(self, begin: Expr, end: Expr) -> ErrorPos:
        return ErrorPos(begin.pos.lS, begin.pos.cS, end.pos.lE, end.pos.cE)

    def __peek(self) -> Token:
        return self.tokens[self.__current]

    def __isAtEnd(self) -> bool:
        return self.__peek().tokenType == TokenType.EOF

    def __previous(self) -> Token:
        return self.tokens[self.__current - 1]

    def __advance(self) -> Token:
        if not self.__isAtEnd(): self.__current += 1
        return self.__previous()

    def __check(self, tokenType: TokenType) -> bool:
        if self.__isAtEnd(): return False
        return self.__peek().tokenType == tokenType

    def __match(self, types: list[TokenType]):
        for tokenType in types:
            if self.__check(tokenType):
                self.__advance()
                return True
        return False

    def __error(self, pos: ErrorPos, message: str) -> None:
        self.errorHandler.error(pos, message)
        raise ParseError()

    def __consume(self, tokenType: TokenType) -> Union[Token, None]:
        if self.__check(tokenType):
            return self.__advance()
        return None

    def __checkErrorExpr(self, expr: Expr, operator: Token, message: str) -> bool:
        if isinstance(expr, ErrorExpr):
            self.__error(operator.pos, message)
            return True
        return False

    def __synchronize(self):
        self.__advance()
        while not self.__isAtEnd():
            if self.__previous().tokenType == TokenType.SEMICOLON: return
            if self.__peek().tokenType in (
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.FOR,
                TokenType.VAR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN,
            ) : return
            self.__advance()

    def __primary(self) -> Expr:
        if self.__match([TokenType.FALSE]):
            return Literal(PLObject(PLObjType.BOOL, False), self.__posFromTokens())
        if self.__match([TokenType.TRUE]):
            return Literal(PLObject(PLObjType.BOOL, True), self.__posFromTokens())
        if self.__match([TokenType.NIL]):
            return Literal(PLObject(PLObjType.NIL, None), self.__posFromTokens())

        if self.__match([TokenType.STRING]):
            return Literal(PLObject(PLObjType.STRING, self.__previous().literal),
            self.__posFromTokens())
        if self.__match([TokenType.NUMBER]):
            return Literal(PLObject(PLObjType.NUMBER, self.__previous().literal),
            self.__posFromTokens())

        if self.__match([TokenType.IDENTIFIER]):
            return Variable(self.__previous(), self.__posFromTokens())

        if self.__match([TokenType.LEFT_PAREN]):
            openingBracket = self.__previous()
            expr = self.__expression()
            if self.__consume(TokenType.RIGHT_PAREN) == None:
                self.__error(openingBracket.pos, "Expected closing bracket")
            return Grouping(expr, self.__posFromTokens(openingBracket, self.__previous()))

        return ErrorExpr(self.__posFromTokens())

    def __unary(self) -> Expr:
        if self.__match([TokenType.BANG, TokenType.MINUS]):
            operator = self.__previous()
            right = self.__unary()
            if self.__checkErrorExpr(right, operator, f"Unary operator {operator.lexeme} expected operand"):
                return ErrorExpr(self.__posFromTokens())
            return Unary(operator, right, self.__posTokenToExpr(operator, right))
        return self.__primary()

    def __factor(self) -> Expr:
        expr = self.__unary()
        while self.__match([TokenType.SLASH, TokenType.STAR]):
            operator = self.__previous()
            right = self.__unary()
            self.__checkErrorExpr(expr, operator, f"Binary operator {operator.lexeme} expected left operand")
            self.__checkErrorExpr(right, operator, f"Binary operator {operator.lexeme} expected right operand")
            expr = Binary(expr, operator, right, self.__posFromExprs(expr, right))
        return expr

    def __term(self) -> Expr:
        expr = self.__factor()
        while self.__match([TokenType.MINUS, TokenType.PLUS]):
            operator = self.__previous()
            right = self.__factor()
            self.__checkErrorExpr(expr, operator, f"Binary operator {operator.lexeme} expected left operand")
            self.__checkErrorExpr(right, operator, f"Binary operator {operator.lexeme} expected right operand")
            expr = Binary(expr, operator, right, self.__posFromExprs(expr, right))
        return expr

    def __comparison(self) -> Expr:
        expr = self.__term()
        while self.__match([TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL]):
            operator = self.__previous()
            right = self.__term()
            self.__checkErrorExpr(expr, operator, f"Binary operator {operator.lexeme} expected left operand")
            self.__checkErrorExpr(right, operator, f"Binary operator {operator.lexeme} expected right operand")
            expr = Binary(expr, operator, right, self.__posFromExprs(expr, right))
        return expr

    def __equality(self) -> Expr:
        expr = self.__comparison()
        while self.__match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]):
            operator = self.__previous()
            right = self.__comparison()
            self.__checkErrorExpr(expr, operator, f"Binary operator {operator.lexeme} expected left operand")
            self.__checkErrorExpr(right, operator, f"Binary operator {operator.lexeme} expected right operand")
            expr = Binary(expr, operator, right, self.__posFromExprs(expr, right))
        return expr

    def __ternary(self) -> Expr:
        expr = self.__equality()
        if self.__match([TokenType.QUERY]):
            leftOp = self.__previous()
            midExpr = self.__equality()
            rightOp = self.__consume(TokenType.COLON)
            right = self.__equality()
            if not rightOp:
                self.__error(leftOp.pos, "Ternary operator expected colon")
                rightOp = Token(TokenType.ERROR, "ERROR", "", leftOp.line, leftOp.char)
            self.__checkErrorExpr(expr, leftOp, f"Ternary operator {leftOp.lexeme} expected condition")
            self.__checkErrorExpr(midExpr, rightOp, f"Ternary operator {rightOp.lexeme} expected left operand")
            self.__checkErrorExpr(right, rightOp, f"Ternary operator {rightOp.lexeme} expected right operand")
            expr = Ternary(expr, leftOp, midExpr, rightOp, right, self.__posFromExprs(expr, right))
        return expr

    def __and(self) -> Expr:
        expr = self.__ternary()
        while self.__match([TokenType.AND]):
            operator = self.__previous()
            right = self.__ternary()
            self.__checkErrorExpr(expr, operator, f"Logical operator {operator.lexeme} expected left operand")
            self.__checkErrorExpr(right, operator, f"Logical operator {operator.lexeme} expected right operand")
            expr = Logical(expr, operator, right, self.__posFromExprs(expr, right))
        return expr

    def __or(self) -> Expr:
        expr = self.__and()
        while self.__match([TokenType.OR]):
            operator = self.__previous()
            right = self.__and()
            self.__checkErrorExpr(expr, operator, f"Logical operator {operator.lexeme} expected left operand")
            self.__checkErrorExpr(right, operator, f"Logical operator {operator.lexeme} expected right operand")
            expr = Logical(expr, operator, right, self.__posFromExprs(expr, right))
        return expr

    def __assignment(self) -> Expr:
        expr = self.__or()
        if self.__match([TokenType.EQUAL]):
            value = self.__or()
            if isinstance(expr, Variable):
                name = expr.name
                return Assignment(name, value, self.__posFromExprs(expr, value))
            else:
                self.__error(self.__posFromExprs(expr, value), f"Invalid assignment target")
        return expr

    def __expression(self) -> Expr:
        expr = self.__assignment()
        while self.__match([TokenType.COMMA]):
            operator = self.__previous()
            right = self.__assignment()
            self.__checkErrorExpr(expr, operator, f"Binary operator {operator.lexeme} expected left operand")
            self.__checkErrorExpr(right, operator, f"Binary operator {operator.lexeme} expected right operand")
            expr = Binary(expr, operator, right, self.__posFromExprs(expr, right))
        self.__checkErrorExpr(expr, Token(TokenType.ERROR, "", "", 0, 0), "Expected expression")
        return expr

    def __printStatement(self) -> Stmt:
        printKwd = self.__previous()
        value: Expr = self.__expression()
        if self.__consume(TokenType.SEMICOLON) == None:
                self.__error(self.__posTokenToExpr(printKwd, value), "Expected semicolon")
        return PrintStmt(value)

    def __blockStatement(self) -> Stmt:
        leftParen = self.__previous()
        statements: list[Stms] = []
        while not self.__check(TokenType.RIGHT_BRACE) and not self.__isAtEnd():
            statements.append(self.__declaration())
        if self.__consume(TokenType.RIGHT_BRACE) == None:
            #TODO: Add position to statements
            self.__error(self.__posTokenToExpr(leftParen, leftParen), "Expected closing brace")
        return BlockStmt(statements)

    def __expressionStatement(self) -> Stmt:
        expr: Expr = self.__expression()
        if self.__consume(TokenType.SEMICOLON) == None:
                self.__error(expr.pos, "Expected semicolon")
        return ExprStmt(expr)

    def __variableStatement(self) -> Stmt:
        varKwd = self.__previous()
        name: Token = self.__consume(TokenType.IDENTIFIER)
        initializer = None
        if name == None:
            self.__error(varKwd.pos, "Expected variable name")
        if self.__match([TokenType.EQUAL]):
            initializer = self.__expression()
        if self.__consume(TokenType.SEMICOLON) == None:
                self.__error(self.__posTokenToExpr(varKwd, initializer if initializer != None else name), "Expected semicolon")
        return VarStmt(name, initializer)

    def __ifStatement(self) -> Stmt:
        ifKwd = self.__previous()
        if self.__consume(TokenType.LEFT_PAREN) == None:
            self.__error(self.__posFromTokens(ifKwd, ifKwd), "Expected '(' after 'if'")
        condition = self.__expression()
        if self.__consume(TokenType.RIGHT_PAREN) == None:
            self.__error(self.__posFromTokens(ifKwd, ifKwd), "Expected ')' after if-condition")
        thenBranch = self.__statement()
        elseBranch = None
        if self.__match([TokenType.ELSE]):
            elseBranch = self.__statement()
        return IfStmt(condition, thenBranch, elseBranch)
        
    def __statement(self) -> Stmt:
        if self.__match([TokenType.PRINT]):
            return self.__printStatement()
        elif self.__match([TokenType.LEFT_BRACE]):
            return self.__blockStatement()
        elif self.__match([TokenType.IF]):
            return self.__ifStatement()
        return self.__expressionStatement()

    def __declaration(self) -> Stmt:
        try:
            if self.__match([TokenType.VAR]):
                return self.__variableStatement()
            return self.__statement()
        except ParseError:
            self.__synchronize()
            return ErrorStmt()

    def parse(self) -> list[Stmt]:
        statements: list[Stmt] = []
        while not self.__isAtEnd():
            statements.append(self.__declaration())
        return statements