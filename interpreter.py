from expr import Binary, Expr, Grouping, Literal, Unary, Visitor
from langtypes import Bool, LoxType, Number, String
from tokens import TokenType


class Interpreter(Visitor[LoxType]):
    def evaluate(self, expr: Expr) -> LoxType:
        return expr.accept(self)

    def visit_literal(self, literal: Literal) -> LoxType:
        return literal.value

    def visit_grouping(self, grouping: Grouping) -> LoxType:
        return self.evaluate(grouping.expression)

    def visit_unary(self, unary: Unary) -> LoxType:
        right = self.evaluate(unary.right)
        match (unary.operator.type, right):
            case (TokenType.MINUS, Number(r)):
                return Number(r * -1)
            case (TokenType.BANG, r):
                return Bool(not _is_truthy(r))
            case _:
                raise ValueError(f"invalid unary expression: {unary}")

    def visit_binary(self, binary: Binary) -> LoxType:
        left = self.evaluate(binary.left)
        right = self.evaluate(binary.right)
        match (binary.operator.type, left, right):
            case (TokenType.MINUS, Number(l), Number(r)):
                return Number(l - r)
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
            case (TokenType.EQUAL_EQUAL, l, r):
                return Bool(_is_equal(l, r))
            case (TokenType.BANG_EQUAL, l, r):
                return Bool(not _is_equal(l, r))
            case (_, _, _):
                raise ValueError(f"invalid binary operator: {binary}")


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
