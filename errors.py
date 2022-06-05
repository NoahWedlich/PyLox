class ErrorHandler:
    def __init__(self) -> None:
        self.hadError = False

    def error(self, line: int, message: str) -> None:
        self.hadError = True
        print(f"[ERROR] at line {line}: {message}")