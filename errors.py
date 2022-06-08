from typing import Tuple
from tokens import Token

class PyLoxRuntimeError(Exception):
    def __init__(self, token: Token, message: str) -> None:
        self.token = token
        self.message = message
        super().__init__(self.message)

class ErrorHandler:
    def __init__(self) -> None:
        self.hadError = False
        self.hadRuntimeError = False
        self.__errors: list[Tuple[int, int, str, int]] = []

    def error(self, line: int, char: int, message: str, offset: int = 0) -> None:
        self.__errors.append((line, char, message, offset))
        self.hadError = True

    def runtimeError(self, runtimeError: PyLoxRuntimeError) -> None:
        token = runtimeError.token
        self.__errors.append((token.line, token.char, runtimeError.message, 0))
        self.hadRuntimeError = True

    def reportErrors(self, sourceCode: str) -> bool:
        if self.hadError or self.hadRuntimeError:
            sourceLines = sourceCode.split("\n")
            for error in self.__errors:
                line, char, message, offset = error
                source = sourceLines[line-1]#[0:char + offset]
                linePrefix = str(line) + " | "
                print(f"Error: {message}\n")
                print(f"\t{linePrefix}{source}")
                print("\t" + " "*len(linePrefix) + " "*(char-1) + "^--here")
            self.__errors = []
            return True
        return False