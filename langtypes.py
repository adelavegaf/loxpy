from dataclasses import dataclass


type LoxType = Bool | Number | String | None


@dataclass(frozen=True)
class Bool:
    value: bool

    def __repr__(self) -> str:
        return repr(self.value).lower()


@dataclass(frozen=True)
class Number:
    value: float

    def __repr__(self) -> str:
        return repr(int(self.value)) if self.value.is_integer() else repr(self.value)


@dataclass(frozen=True)
class String:
    value: str

    def __repr__(self) -> str:
        return self.value
