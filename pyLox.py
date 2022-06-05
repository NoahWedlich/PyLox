import sys
from scanner import Scanner
from errors import ErrorHandler

def run(source: str, errorHandler: ErrorHandler) -> None:
    scanner = Scanner(source, errorHandler)
    tokens = scanner.scanTokens()
    if errorHandler.hadError: return
    scanner.dumpTokens()

def runFile(file: str, errorHandler: ErrorHandler) -> None:
    with open(file, "r") as f:
        source = f.read()
        if not run(source, errorHandler):
            exit(1)

def runRepl(errorHandler: ErrorHandler) -> None:
    print("PyLox REPL:")
    while True:
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

if __name__ == '__main__':
    pyLox()