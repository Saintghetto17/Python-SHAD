import copy
from collections import UserList
import typing as tp


class ListTwist(UserList[tp.Any]):
    """
    List-like class with additional attributes:
        * reversed, R - return reversed list
        * first, F - insert or retrieve first element;
                     Undefined for empty list
        * last, L -  insert or retrieve last element;
                     Undefined for empty list
        * size, S -  set or retrieve size of list;
                     If size less than list length - truncate to size;
                     If size greater than list length - pad with Nones
    """

    def __init__(self, elements: tp.Any = None):
        super().__init__(elements)

    # operator '.'
    def __getattr__(self, item: str) -> tp.Any:
        if item == 'reversed' or item == 'R':
            rev: list[tp.Any] = copy.deepcopy(self.data)
            rev.reverse()
            return rev
        elif item == 'first' or item == 'F':
            return self.data[0]
        elif item == 'last' or item == 'L':
            return self.data[-1]
        elif item == 'size' or item == 'S':
            return len(self.data)
        else:
            return None

    def __setattr__(self, key: str, value: tp.Any) -> None:
        if key == 'data':
            self.__dict__[key] = value
            return
        if key == 'F' or key == 'first':
            self.data[0] = value
        if key == 'L' or key == 'last':
            self.data[len(self.data) - 1] = value
        if key == 'size' or key == 'S':
            elem: list[tp.Any] = []
            if self.size is not None:
                if self.size >= value:
                    elem = self.data[:value]
                else:
                    elem = copy.deepcopy(self.data)
                    for i in range(value - self.size):
                        elem.append(None)
            self.data = copy.deepcopy(elem)
