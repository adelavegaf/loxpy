from pathlib import Path
from error import Error
import sys

from scanner import Scanner


def main() -> None:
    match sys.argv[1:]:
        case []:
            run_prompt()
        case [path]:
            run_file(Path(path))
        case [*_args]:
            print("Usage: pylox [script]")
            sys.exit(64)


def run_prompt():
    while True:
        try:
            line = input("> ")
            run(line)
            Error.had_error = False
        except EOFError:
            break


def run_file(file: Path) -> None:
    with open(file, "rb") as f:
        contents = f.read()
        run(contents.decode())
        if Error.had_error:
            sys.exit(65)


def run(source: str) -> None:
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    # TODO: we should handle errors
    for token in tokens:
        print(token)


if __name__ == "__main__":
    main()
