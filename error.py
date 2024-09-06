from dataclasses import dataclass
from tokens import Token, TokenType


@dataclass
class RuntimeErr(Exception):
    token: Token
    message: str


class Error:
    had_error: bool = False
    had_runtime_error: bool = False

    @classmethod
    def error(cls, line: int, message: str) -> None:
        cls._report(line, "", message)

    @classmethod
    def runtime_error(cls, err: RuntimeErr) -> None:
        cls.had_runtime_error = True
        print(f"{err.message}\n[line {err.token.line}]")

    @classmethod
    def parse_error(cls, token: Token, message: str) -> None:
        if token.type is TokenType.EOF:
            cls._report(token.line, "at end", message)
        else:
            cls._report(token.line, f"at '{token.lexeme}'", message)

    @classmethod
    def _report(cls, line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error{where}: {message}")
        cls.had_error = True
