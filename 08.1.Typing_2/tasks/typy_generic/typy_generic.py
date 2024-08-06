import typing as tp

T = tp.TypeVar('T', float, int)


class Pair(tp.Generic[T]):
    def __init__(self, a: T, b: T) -> None:
        self.a: T = a
        self.b: T = b

    def sum(self) -> T:
        return self.a + self.b

    def first(self) -> T:
        return self.a

    def second(self) -> T:
        return self.b

    def __iadd__(self, pair: "Pair[T]") -> "Pair[T]":
        a_new: T = self.a + pair.a
        b_new: T = self.b + pair.b
        return Pair[T](a_new, b_new)
