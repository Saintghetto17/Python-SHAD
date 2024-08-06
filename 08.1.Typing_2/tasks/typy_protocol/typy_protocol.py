from typing import Protocol, TypeVar

T_co = TypeVar("T_co", covariant=True)


class Gettable(Protocol[T_co]):
    def __getitem__(self, item: int) -> T_co:
        pass

    def __len__(self) -> int:
        pass


def get(container: Gettable[T_co] | None, index: int) -> T_co | None:
    if container:
        return container[index]

    return None
