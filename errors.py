class ErrorHandler:
    def __init__(self) -> None:
        self.hadError = False
        self.__errors: list[Tuple[int, int, str, int]] = []

    def error(self, line: int, char: int, message: str, offset: int = 0) -> None:
        self.__errors.append((line, char, message, offset))
        self.hadError = True

    def reportErrors(self, sourceCode: str):
        sourceLines = sourceCode.split("\n")
        for error in self.__errors:
            line, char, message, offset = error
            source = sourceLines[line-1][0:char + offset]
            linePrefix = str(line) + " | "
            print(f"Error: {message}\n")
            print(f"\t{linePrefix}{source}")
            print("\t" + " "*len(linePrefix) + " "*(char-1) + "^--here")
        self.__errors = []