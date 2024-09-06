from pathlib import Path
from error import Error
import sys

from interpreter import Interpreter
from parser import Parser
from scanner import Scanner


def main() -> None:
    interpreter = Interpreter()
    match sys.argv[1:]:
        case []:
            run_prompt(interpreter)
        case [path]:
            run_file(interpreter, Path(path))
        case [*_args]:
            print("Usage: pylox [script]")
            sys.exit(64)


def run_prompt(interpreter: Interpreter):
    while True:
        try:
            line = input("> ")
            run(interpreter, line)
            Error.had_error = False
        except EOFError:
            break


def run_file(interpreter: Interpreter, file: Path) -> None:
    with open(file, "rb") as f:
        contents = f.read()
        run(interpreter, contents.decode())
        if Error.had_error:
            sys.exit(65)
        elif Error.had_runtime_error:
            sys.exit(70)


def run(interpreter: Interpreter, source: str) -> None:
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)
    expression = parser.parse()
    if expression is None:
        return
    interpreter.interpret(expression)


if __name__ == "__main__":
    main()
