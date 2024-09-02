from error import Error
from expr import Binary, Expr, Grouping, Literal, Ternary, Unary
from tokens import Token, TokenType


class ParseError(RuntimeError):
    pass


class Parser:
    """
    comma          → expression ( "," expression )* ;
    ternary        → expression "?" ternary ":" ternary
                   | expression ;
    expression     → equality ;
    equality       → comparison ( ( "!=" | "==" ) comparison )* ;
    comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
    term           → factor ( ( "-" | "+" ) factor )* ;
    factor         → unary ( ( "/" | "*" ) unary )* ;
    unary          → ( "!" | "-" ) unary
                   | primary ;
    primary        → NUMBER | STRING | "true" | "false" | "nil"
                   | "(" expression ")" ;
    """

    def __init__(self, tokens: list[Token]) -> None:
        self._tokens: list[Token] = tokens
        self._current: int = 0

    def parse(self) -> Expr | None:
        try:
            return self._comma()
        except ParseError:
            return None

    def _comma(self) -> Expr:
        left = self._ternary()
        while self._match(TokenType.COMMA):
            operator = self._previous()
            right = self._ternary()
            left = Binary(left, operator, right)
        return left

    def _ternary(self) -> Expr:
        expr = self._expression()
        if self._peek().type == TokenType.QUESTION_MARK:
            self._advance()
            left = self._ternary()
            self._consume(TokenType.COLON, "Expect ':' after expression")
            right = self._ternary()
            return Ternary(expr, left, right)
        else:
            return expr

    def _expression(self) -> Expr:
        return self._equality()

    def _equality(self) -> Expr:
        expr = self._comparison()
        while self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self._previous()
            right = self._comparison()
            expr = Binary(expr, operator, right)

        return expr

    def _comparison(self) -> Expr:
        left = self._term()
        while self._match(
            TokenType.LESS,
            TokenType.LESS_EQUAL,
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
        ):
            operator = self._previous()
            right = self._term()
            left = Binary(left, operator, right)
        return left

    def _term(self) -> Expr:
        left = self._factor()
        while self._match(
            TokenType.MINUS,
            TokenType.PLUS,
        ):
            operator = self._previous()
            right = self._factor()
            left = Binary(left, operator, right)
        return left

    def _factor(self) -> Expr:
        left = self._unary()
        while self._match(
            TokenType.STAR,
            TokenType.SLASH,
        ):
            operator = self._previous()
            right = self._unary()
            left = Binary(left, operator, right)
        return left

    def _unary(self) -> Expr:
        if self._match(TokenType.BANG, TokenType.MINUS):
            operator = self._previous()
            right = self._unary()
            return Unary(operator, right)
        else:
            return self._primary()

    def _primary(self) -> Expr:
        if self._match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self._previous().literal)
        elif self._match(TokenType.FALSE):
            return Literal(False)
        elif self._match(TokenType.TRUE):
            return Literal(True)
        elif self._match(TokenType.NIL):
            return Literal(None)
        elif self._match(TokenType.LEFT_PAREN):
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        else:
            raise self._error(self._peek(), "Expect expression.")

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

    def _advance(self) -> Token:
        if not self._is_at_end():
            self._current += 1
        return self._previous()

    def _is_at_end(self):
        return self._peek().type == TokenType.EOF

    def _peek(self) -> Token:
        return self._tokens[self._current]

    def _previous(self) -> Token:
        return self._tokens[self._current - 1]

    def _consume(self, token_type: TokenType, message: str) -> Token:
        if self._check(token_type):
            return self._advance()
        raise self._error(self._peek(), message)

    def _error(self, token: Token, message: str) -> ParseError:
        Error.parse_error(token, message)
        return ParseError()

    def _synchronize(self) -> None:
        self._advance()

        while not self._is_at_end():
            if self._previous().type is TokenType.SEMICOLON:
                return

            match self._peek().type:
                case (
                    TokenType.CLASS
                    | TokenType.FUN
                    | TokenType.VAR
                    | TokenType.FOR
                    | TokenType.IF
                    | TokenType.WHILE
                    | TokenType.PRINT
                    | TokenType.RETURN
                ):
                    return
                case _:
                    self._advance()
