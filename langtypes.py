from dataclasses import dataclass


type LoxType = Bool | Number | String | None


@dataclass(frozen=True)
class Bool:
    value: bool


@dataclass(frozen=True)
class Number:
    value: float


@dataclass(frozen=True)
class String:
    value: str
