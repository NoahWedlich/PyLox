from ftplib import error_perm
import sys
from expr import Expr, Binary, Unary, Literal, Grouping, AstPrinter
from tokens import Token, TokenType
from scanner import Scanner
from parser import Parser
from analyzer import Analyzer
from interpreter import Interpreter
from errors import ErrorHandler

def run(source: str, analyzer: Analyzer, interpreter: Interpreter, errorHandler: ErrorHandler) -> None:
    scanner = Scanner(source, errorHandler)
    tokens = scanner.scanTokens()
    errorHandler.reportErrors(source)

    parser = Parser(tokens, errorHandler)
    program = parser.parse()
    if errorHandler.reportErrors(source):
        return
    
    analyzer.typeCheckProgram(program)
    if errorHandler.reportErrors(source):
        return

    interpreter.interpret(program)
    errorHandler.reportErrors(source)

def runFile(file: str, analyzer: Analyzer, interpreter: Interpreter, errorHandler: ErrorHandler) -> None:
    with open(file, "r") as f:
        source = f.read()
        if run(source, analyzer, interpreter, errorHandler):
            if errorHandler.hadError:
                exit(65)
            elif ErrorHandler.hadRuntimeError:
                exit(70)

def runRepl(analyzer: Analyzer, interpreter: Interpreter, errorHandler: ErrorHandler) -> None:
    print("PyLox REPL:")
    while True:
        errorHandler.hadError = False
        errorHandler.hadRuntimeError = False
        line = input("> ")
        if line == "" or line == "exit": break
        run(line, analyzer, interpreter, errorHandler)

def pyLox():
    errorHandler = ErrorHandler()
    analyzer = Analyzer(errorHandler)
    interpreter = Interpreter(errorHandler)
    if len(sys.argv) > 2:
        print("Usage: python pyLox.py [script]")
        exit(1)
    elif len(sys.argv) == 2:
        runFile(sys.argv[1], analyzer, interpreter, errorHandler)
    else:
        runRepl(analyzer, interpreter, errorHandler)

def tempMain():
    expr = Binary(Unary(Token(TokenType.MINUS, "-", "", 1), Literal(123)), 
           Token(TokenType.STAR, "*", "", 1), 
           Grouping(Literal(45.67)))
    print(AstPrinter().print(expr))

if __name__ == '__main__':
    pyLox()
    # tempMain()