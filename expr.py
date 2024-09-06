from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from langtypes import LoxType
from tokens import Token


class Expr(ABC):
    @abstractmethod
    def accept[R](self, visitor: Visitor[R]) -> R: ...


@dataclass
class Ternary(Expr):
    cmp: Expr
    left: Expr
    right: Expr

    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_ternary(self)


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_binary(self)


@dataclass
class Grouping(Expr):
    expression: Expr

    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_grouping(self)


@dataclass
class Literal(Expr):
    value: LoxType

    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_literal(self)


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_unary(self)


class Visitor[R](ABC):
    @abstractmethod
    def visit_ternary(self, ternary: Ternary) -> R: ...

    @abstractmethod
    def visit_binary(self, binary: Binary) -> R: ...

    @abstractmethod
    def visit_grouping(self, grouping: Grouping) -> R: ...

    @abstractmethod
    def visit_literal(self, literal: Literal) -> R: ...

    @abstractmethod
    def visit_unary(self, unary: Unary) -> R: ...
