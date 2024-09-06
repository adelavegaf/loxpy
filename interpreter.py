from error import Error, RuntimeErr
from expr import Binary, Expr, Grouping, Literal, Ternary, Unary, Visitor
from langtypes import Bool, LoxType, Number, String
from tokens import TokenType


class Interpreter(Visitor[LoxType]):
    def interpret(self, expr: Expr) -> None:
        try:
            value = self._evaluate(expr)
            print(_stringify(value))
        except RuntimeErr as err:
            Error.runtime_error(err)

    def _evaluate(self, expr: Expr) -> LoxType:
        return expr.accept(self)

    def visit_literal(self, literal: Literal) -> LoxType:
        return literal.value

    def visit_grouping(self, grouping: Grouping) -> LoxType:
        return self._evaluate(grouping.expression)

    def visit_unary(self, unary: Unary) -> LoxType:
        right = self._evaluate(unary.right)
        match (unary.operator.type, right):
            case (TokenType.MINUS, Number(r)):
                return Number(r * -1)
            case (TokenType.BANG, r):
                return Bool(not _is_truthy(r))
            case (_, right):
                lexeme = unary.operator.lexeme
                rclass = right.__class__.__name__.lower()
                raise RuntimeErr(
                    unary.operator,
                    f"unary operator '{lexeme}' can't be applied to {rclass}",
                )

    def visit_binary(self, binary: Binary) -> LoxType:
        left = self._evaluate(binary.left)
        right = self._evaluate(binary.right)
        match (binary.operator.type, left, right):
            case (TokenType.MINUS, Number(l), Number(r)):
                return Number(l - r)
            case (TokenType.SLASH, Number(l), Number(0)):
                raise RuntimeErr(binary.operator, "division by 0")
            case (TokenType.SLASH, Number(l), Number(r)):
                return Number(l / r)
            case (TokenType.STAR, Number(l), Number(r)):
                return Number(l * r)
            case (TokenType.GREATER, Number(l), Number(r)):
                return Bool(l > r)
            case (TokenType.GREATER_EQUAL, Number(l), Number(r)):
                return Bool(l >= r)
            case (TokenType.LESS, Number(l), Number(r)):
                return Bool(l < r)
            case (TokenType.LESS_EQUAL, Number(l), Number(r)):
                return Bool(l <= r)
            case (TokenType.PLUS, Number(l), Number(r)):
                return Number(l + r)
            case (TokenType.PLUS, String(l), String(r)):
                return String(l + r)
            case (TokenType.PLUS, String(l), r):
                return String(l + _stringify(r))
            case (TokenType.PLUS, l, String(r)):
                return String(_stringify(l) + r)
            case (TokenType.EQUAL_EQUAL, l, r):
                return Bool(_is_equal(l, r))
            case (TokenType.BANG_EQUAL, l, r):
                return Bool(not _is_equal(l, r))
            case (_, l, r):
                lexeme = binary.operator.lexeme
                lclass = l.__class__.__name__.lower()
                rclass = r.__class__.__name__.lower()
                raise RuntimeErr(
                    binary.operator,
                    f"binary operator '{lexeme}' can't be applied to {lclass} and {rclass}",
                )

    def visit_ternary(self, ternary: Ternary) -> LoxType:
        cmp = self._evaluate(ternary.cmp)
        return (
            self._evaluate(ternary.left)
            if _is_truthy(cmp)
            else self._evaluate(ternary.right)
        )


def _is_truthy(value: LoxType) -> bool:
    match value:
        case Bool(b):
            return b
        case None:
            return False
        case _:
            return True


def _is_equal(a: LoxType, b: LoxType) -> bool:
    match (a, b):
        case (None, None):
            return True
        case (String(s1), String(s2)):
            return s1 == s2
        case (Number(n1), Number(n2)):
            return n1 == n2
        case (Bool(b1), Bool(b2)):
            return b1 == b2
        case (_, _):
            return False


def _stringify(value: LoxType) -> str:
    match value:
        case None:
            return "nil"
        case other:
            return repr(other)
