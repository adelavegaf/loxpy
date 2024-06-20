class Error:
    had_error: bool = False

    @classmethod
    def error(cls, line: int, message: str) -> None:
        cls._report(line, "", message)

    @classmethod
    def _report(cls, line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error{where}: {message}")
        cls.had_error = True
