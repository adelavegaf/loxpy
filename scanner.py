from error import Error
from tokens import Token, TokenType


KEYWORDS: dict[str, TokenType] = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}


class Scanner:
    def __init__(self, source: str) -> None:
        self.source: str = source
        self.tokens: list[Token] = []
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self):
        c = self.advance()
        match c:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
            case ",":
                self.add_token(TokenType.COMMA)
            case ".":
                self.add_token(TokenType.DOT)
            case "-":
                self.add_token(TokenType.MINUS)
            case "+":
                self.add_token(TokenType.PLUS)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case "*":
                self.add_token(TokenType.STAR)
            case "?":
                self.add_token(TokenType.QUESTION_MARK)
            case ":":
                self.add_token(TokenType.COLON)
            # ambiguous one or two character tokens
            case "!":
                if self.match("="):
                    self.add_token(TokenType.BANG_EQUAL)
                else:
                    self.add_token(TokenType.BANG)
            case "=":
                if self.match("="):
                    self.add_token(TokenType.EQUAL_EQUAL)
                else:
                    self.add_token(TokenType.EQUAL)
            case "<":
                if self.match("="):
                    self.add_token(TokenType.LESS_EQUAL)
                else:
                    self.add_token(TokenType.LESS)
            case ">":
                if self.match("="):
                    self.add_token(TokenType.GREATER_EQUAL)
                else:
                    self.add_token(TokenType.GREATER)
            case "/":
                if self.match("/"):
                    while not self.is_at_end() and self.peek() != "\n":
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case "/":
                self.add_token(TokenType.SLASH)
            # literals
            case '"':
                self.string()
            case d if is_digit(d):
                self.number()
            # identifiers
            case a if is_alpha(a):
                self.identifier()
            case "\n":
                self.line += 1
            # meaningless characters:
            case " " | "\r" | "\t":
                pass
            case _:
                Error.error(self.line, "Unexpected character")

    def add_token(self, token_type: TokenType, literal: object = None) -> None:
        token = Token(
            token_type, self.source[self.start : self.current], literal, self.line
        )
        self.tokens.append(token)

    def string(self) -> None:
        while not self.is_at_end() and self.peek() != '"':
            c = self.advance()
            if c == "\n":
                self.line += 1

        if self.is_at_end():
            Error.error(self.line, "Unterminated string")
            return

        # consume "
        self.advance()
        literal = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, literal)

    def number(self) -> None:
        while is_digit(self.peek()):
            self.advance()

        if self.peek() == "." and is_digit(self.peek_next()):
            self.advance()
            while is_digit(self.peek()):
                self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def identifier(self) -> None:
        while is_alphanumeric(self.peek()):
            self.advance()

        value = self.source[self.start : self.current]
        token_type = KEYWORDS.get(value) or TokenType.IDENTIFIER
        self.add_token(token_type)

    def advance(self) -> str:
        c = self.source[self.current]
        self.current += 1
        return c

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False

        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        else:
            return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        else:
            return self.source[self.current + 1]

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)


def is_digit(d: str) -> bool:
    match d:
        case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9":
            return True
        case _:
            return False


def is_alpha(a: str) -> bool:
    match a:
        case (
            "_"
            | "a"
            | "b"
            | "c"
            | "d"
            | "e"
            | "f"
            | "g"
            | "h"
            | "i"
            | "j"
            | "k"
            | "l"
            | "m"
            | "n"
            | "o"
            | "p"
            | "q"
            | "r"
            | "s"
            | "t"
            | "u"
            | "v"
            | "w"
            | "x"
            | "y"
            | "z"
            | "A"
            | "B"
            | "C"
            | "D"
            | "E"
            | "F"
            | "G"
            | "H"
            | "I"
            | "J"
            | "K"
            | "L"
            | "M"
            | "N"
            | "O"
            | "P"
            | "Q"
            | "R"
            | "S"
            | "T"
            | "U"
            | "V"
            | "W"
            | "X"
            | "Y"
            | "Z"
        ):
            return True
        case _:
            return False


def is_alphanumeric(a: str) -> bool:
    return is_digit(a) or is_alpha(a)
