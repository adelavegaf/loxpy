import sys


def main() -> None:
    [_bin, *args] = sys.argv
    match len(args):
        case 0:
            run_prompt()
        case 1:
            run_file()
        case _:
            print("Usage: pylox [script]")


def run_prompt():
    pass


def run_file():
    pass


if __name__ == "__main__":
    main()
