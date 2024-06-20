from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    # Single-character tokens
    LEFT_PAREN = 0
    RIGHT_PAREN = 1
    LEFT_BRACE = 2
    RIGHT_BRACE = 3
    COMMA = 4
    DOT = 5
    MINUS = 6
    PLUS = 7
    SEMICOLON = 8
    SLASH = 9
    STAR = 10

    # One or two character tokens
    BANG = 11
    BANG_EQUAL = 12
    EQUAL = 12
    EQUAL_EQUAL = 13
    GREATER = 14
    GREATER_EQUAL = 15
    LESS = 16
    LESS_EQUAL = 17

    # Literals
    IDENTIFIER = 18
    STRING = 19
    NUMBER = 20

    # Keywords
    AND = 21
    CLASS = 22
    ELSE = 23
    FALSE = 24
    FUN = 25
    FOR = 26
    IF = 27
    NIL = 28
    OR = 29
    PRINT = 30
    RETURN = 31
    SUPER = 32
    THIS = 33
    TRUE = 34
    VAR = 35
    WHILE = 36

    EOF = 37


@dataclass(repr=False)
class Token:
    type: TokenType
    lexeme: str
    literal: object
    line: int

    def __repr__(self) -> str:
        return f"{self.type} {self.lexeme} {self.literal}"
