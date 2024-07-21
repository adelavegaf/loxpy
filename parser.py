from typing import Callable
from expr import Binary, Expr, Grouping, Literal, Unary
from tokens import Token, TokenType


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self._tokens: list[Token] = tokens
        self._current: int = 0

    def _expression(self) -> Expr:
        return self._equality()

    def _equality(self) -> Expr:
        expr = self._comparison()
        while match(BANG_EQUAL, EQUAL_EQUAL):
            operator = self._previous()
            right = self._comparison()
            expr = Binary(expr, operator, right)

        return expr

    def _comparison(self) -> Expr:
        pass

    def _match(self, *args: TokenType) -> bool:
        for token in args:
            if self._check(token):
                self._advance()
                return True
        return False

    def _check(self, token_type: TokenType) -> bool:
        if self._is_at_end():
            return False

        return self._peek().type == token_type

    def _peek(self):
        pass

    def _advance(self) -> None:
        if not self._is_at_end():
            self._current += 1
        return self._previous()

    def _previous(self) -> Token:
        pass


# type ParserResult = tuple[list[Token], Expr]


def expression(input: list[Token]) -> Expr:
    return equality(input)


def equality(input: list[Token]) -> Expr:
    left = comparison(input)
    while operator := any_type(input, TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
        right = comparison(input)
        left = Binary(left, operator, right)
    return left


def comparison(input: list[Token]) -> Expr:
    left = term(input)
    while operator := any_type(
        input,
        TokenType.LESS,
        TokenType.LESS_EQUAL,
        TokenType.GREATER,
        TokenType.GREATER_EQUAL,
    ):
        right = term(input)
        left = Binary(left, operator, right)
    return left


def term(input: list[Token]) -> Expr:
    left = factor(input)
    while operator := any_type(
        input,
        TokenType.MINUS,
        TokenType.PLUS,
    ):
        right = factor(input)
        left = Binary(left, operator, right)
    return left


def factor(input: list[Token]) -> Expr:
    left = unary(input)
    while operator := any_type(
        input,
        TokenType.STAR,
        TokenType.SLASH,
    ):
        right = unary(input)
        left = Binary(left, operator, right)
    return left


def unary(input: list[Token]) -> Expr:
    if operator := any_type(input, TokenType.BANG, TokenType.MINUS):
        right = unary(input)
        return Unary(operator, right)
    else:
        return primary(input)


def primary(input: list[Token]) -> Expr:
    if token := any_type(input, TokenType.NUMBER, TokenType.STRING):
        return Literal(token.literal)
    elif type_literal(input, TokenType.FALSE):
        return Literal(False)
    elif type_literal(input, TokenType.TRUE):
        return Literal(True)
    elif type_literal(input, TokenType.NIL):
        return Literal(None)
    elif token := type_literal(input, TokenType.LEFT_PAREN):
        expr = expression(input)
        if not type_literal(input, TokenType.RIGHT_PAREN):
            raise ValueError("Expect ')' after expression.")
        return Grouping(expr)
    else:
        raise ValueError("Uknown expression")


# Combinators


def any_type(input: list[Token], *types: TokenType) -> Token | None:
    for t in types:
        if token := type_literal(input, t):
            return token
    return None


def type_literal(input: list[Token], type_literal: TokenType) -> Token | None:
    next = peek(input)
    if next and next.type is type_literal:
        return input.pop(0)
    else:
        return None


def peek(input: list[Token]) -> Token | None:
    return input[0] if len(input) else None
