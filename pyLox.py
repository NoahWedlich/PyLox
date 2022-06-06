import sys
from expr import Expr, Binary, Unary, Literal, Grouping, AstPrinter
from tokens import Token, TokenType
from scanner import Scanner
from parser import Parser
from errors import ErrorHandler

def run(source: str, errorHandler: ErrorHandler) -> None:
    scanner = Scanner(source, errorHandler)
    tokens = scanner.scanTokens()
    # scanner.dumpTokens()
    parser = Parser(tokens, errorHandler)
    expr = parser.parse()
    if errorHandler.hadError:
        errorHandler.reportErrors(source)
    print(AstPrinter().print(expr))

def runFile(file: str, errorHandler: ErrorHandler) -> None:
    with open(file, "r") as f:
        source = f.read()
        if not run(source, errorHandler):
            exit(1)

def runRepl(errorHandler: ErrorHandler) -> None:
    print("PyLox REPL:")
    while True:
        errorHandler.hadError = False
        line = input("> ")
        if line == "" or line == "exit": break
        run(line, errorHandler)

def pyLox():
    errorHandler = ErrorHandler()
    if len(sys.argv) > 2:
        print("Usage: python pyLox.py [script]")
        exit(1)
    elif len(sys.argv) == 2:
        runFile(sys.argv[1], errorHandler)
    else:
        runRepl(errorHandler)

def tempMain():
    expr = Binary(Unary(Token(TokenType.MINUS, "-", "", 1), Literal(123)), 
           Token(TokenType.STAR, "*", "", 1), 
           Grouping(Literal(45.67)))
    print(AstPrinter().print(expr))

if __name__ == '__main__':
    pyLox()
    # tempMain()