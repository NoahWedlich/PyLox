class ErrorHandler:
    def __init__(self) -> None:
        self.hadError = False

    def error(self, line: int, char: int, message: str, source: str) -> None:
        self.hadError = True
        linePrefix = str(line) + " | "
        print(f"Error: {message}\n")
        print(f"\t{linePrefix}{source}")
        print("\t" + " "*len(linePrefix) + " "*(char-1) + "^--here")