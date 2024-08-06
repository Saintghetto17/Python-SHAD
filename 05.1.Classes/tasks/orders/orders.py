from dataclasses import dataclass, field, InitVar
from abc import ABC, abstractmethod
import typing as tp

DISCOUNT_PERCENTS = 15


@dataclass(frozen=True, order=True)
class Item:
    item_id: int = field(compare=False)
    # note: you might want to change the order of fields
    title: str = field(compare=True)
    cost: int = field(compare=True)

    def __post_init__(self) -> None:
        assert self.cost > 0 and self.title != ''


# You may set `# type: ignore` on this class
# It is [a really old issue](https://github.com/python/mypy/issues/5374)
# But seems to be solved
@dataclass(frozen=True)
class Position(ABC):
    item: Item

    @property
    @abstractmethod
    def cost(self) -> tp.Any:
        pass


@dataclass(frozen=True)
class CountedPosition(Position):
    count: int = 1

    # можем обращаться к _cost и возвращать его
    @property
    def cost(self) -> tp.Any:
        return self.count * self.item.cost


@dataclass(frozen=True)
class WeightedPosition(Position):
    weight: float = 1

    @property
    def cost(self) -> tp.Any:
        return self.weight * self.item.cost


@dataclass
class Order:
    order_id: int
    # mutable objects by default or not should be with field
    positions: list[Position] = field(default_factory=list[Position])
    have_promo: InitVar[bool] = False
    cost: tp.Any = 0

    def __post_init__(self, have_promo: bool) -> None:
        cost = 0
        for pos in self.positions:
            cost += pos.cost
        if have_promo:
            self.cost = int(cost - cost * (DISCOUNT_PERCENTS / 100))
        else:
            self.cost = int(cost)
