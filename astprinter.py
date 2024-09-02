from expr import Binary, Expr, Grouping, Literal, Ternary, Unary, Visitor
from tokens import Token, TokenType


class AstPrinter(Visitor[str]):
    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def visit_ternary(self, ternary: Ternary) -> str:
        return f"(?: {self.print(ternary.cmp)} {self.print(ternary.left)} {self.print(ternary.right)})"

    def visit_binary(self, binary: Binary) -> str:
        return f"({binary.operator.lexeme} {self.print(binary.left)} {self.print(binary.right)})"

    def visit_grouping(self, grouping: Grouping) -> str:
        return f"(group {self.print(grouping.expression)})"

    def visit_literal(self, literal: Literal) -> str:
        if literal.value is None:
            return "nil"
        else:
            return str(literal.value)

    def visit_unary(self, unary: Unary) -> str:
        return f"({unary.operator.lexeme} {self.print(unary.right)})"


if __name__ == "__main__":
    expression = Binary(
        Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(Literal(45.67)),
    )
    print("raw")
    print(expression)
    print("pretty")
    pretty = AstPrinter().print(expression)
    print(pretty)
