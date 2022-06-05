import sys
from scanner import Scanner
from errors import error

def run(source: str) -> bool:
    scanner = Scanner(source)
    tokens, success = scanner.scanTokens()
    scanner.dumpTokens()
    if not success:
        return False

def runFile(file: str) -> None:
    print(f"[INFO] Running file {file}")
    with open(file, "r") as f:
        source = f.read()
        if not run(source):
            exit(1)

def runRepl() -> None:
    print("PyLox REPL:")
    while True:
        line = input("> ")
        if line == "" or line == "exit": break
        run(line)

def pyLox():
    if len(sys.argv) > 2:
        print("Usage: python pyLox.py [script]")
        exit(1)
    elif len(sys.argv) == 2:
        runFile(sys.argv[1])
    else:
        runRepl()

if __name__ == '__main__':
    pyLox()