from typing import Tuple

class ErrorPos():
    def __init__(self, lS: int, cS: int, lE: int, cE: int):
        self.lS: int = lS
        self.cS: int = cS
        self.lE: int = lE
        self.cE: int = cE

    def __str__(self) -> str:
        return f"({self.lS}:{self.cS})"

    def __repr__(self) -> str:
        return f"({self.lS}:{self.cS})->({self.lE}:{self.cE})"

class PyLoxRuntimeError(Exception):
    def __init__(self, pos: ErrorPos, message: str) -> None:
        self.pos = pos
        self.message = message
        super().__init__(self.message)

class ErrorHandler:
    def __init__(self) -> None:
        self.hadError = False
        self.hadRuntimeError = False
        self.__errors: list[Tuple[ErrorPos, str]] = []

    def error(self, pos: ErrorPos, message: str) -> None:
        self.__errors.append((pos, message))
        self.hadError = True

    def runtimeError(self, runtimeError: PyLoxRuntimeError) -> None:
        self.__errors.append((runtimeError.pos, runtimeError.message))
        self.hadRuntimeError = True

    def __printSPosError(self, pos: ErrorPos, message: str, sourceLines: list[str], focus: int = -1) -> None:
        line = pos.lS
        if focus == -1:
            focus = pos.cE
        source = sourceLines[line-1]
        linePrefix = str(line) + " | "
        print(f"Error: {message}\n")
        print(f"\t{linePrefix}{source}")
        print("\t" + " "*len(linePrefix) + " "*(focus-1) + "^--here")

    def __printSLineError(self, pos: ErrorPos, message: str, sourceLines: list[str]) -> None:
        line = pos.lS
        charStart = pos.cS
        charEnd = pos.cE
        source = sourceLines[line-1]
        linePrefix = str(line) + " | "
        print(f"Error: {message}\n")
        print(f"\t{linePrefix}{source}")
        print("\t" + " "*len(linePrefix) + " "*(charStart-1) + "~"*(charEnd - charStart + 1))
        # print("\t" + " "*len(linePrefix) + " "*(focus) + "^--here")

    def __printMPosError(self, pos: ErrorPos, message: str, sourceLines: list[str], focusLine: int = -1, focusChar: int = -1) -> None:
        if focusLine == 0: focusLine = pos.lS
        elif focusLine == -1: focusLine = pos.lE
        if focusChar == -1: focusChar = len(sourceLines[focusLine-1])
        print(f"Error: {message}\n")
        for line in range(pos.lS, pos.lE+1):
            linePrefix = str(line) + " | "
            source = sourceLines[line-1]
            print(f"\t{linePrefix}{source}")
            if line == focusLine:
                print("\t" + " "*len(linePrefix) + " "*(focusChar) + "^--here")

    def reportErrors(self, sourceCode: str) -> bool:
        if self.hadError or self.hadRuntimeError:
            sourceLines = sourceCode.split("\n")
            for error in self.__errors:
                pos, message = error
                if pos.lE - pos.lS > 0:
                    self.__printMPosError(pos, message, sourceLines)
                else:
                    if True:
                        self.__printSPosError(pos, message, sourceLines)
                    else:
                        self.__printSLineError(pos, message, sourceLines)
            self.__errors = []
            return True
        return False