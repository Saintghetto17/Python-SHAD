def problem01() -> dict[int, str]:
    return {5: "Optional -> либо int, либо None, операции + для None нет, mypy ошибка",
            7: "Возвращаемое значение все еще Optional, а не int -> mypy ошибка"}


def problem02() -> dict[int, str]:
    return {
        5: "общий тип листа теперь object (для трех находящихся объектов)   , "
           "у object-a нет оператора +, поэтому ошибка mypy"}


def problem03() -> dict[int, str]:
    return {
        9: "foo принимает mutable generic объект, он инвариантен,"
           " значит можно только int передавать (у нас float), mypy ошибка",
        13: "foo принимает mutable generic объект, он инвариантен,"
            " значит можно только int передавать (у нас bool), mypy ошибка"}


def problem04() -> dict[int, str]:
    return {9: "AbstractSet immutable и поэтому ковариантен по аргументам, значит float предок int-a, но не наоборот"}


def problem05() -> dict[int, str]:
    return {11: "При передаче A() будет ошибка в рантайме, так как возвращаемое значение B, а будет A"}


def problem06() -> dict[int, str]:
    return {
        15: "Атрибут класса потомка должен быть подклассом атрибута предка"
            " (B.values >= C.values), но T предок S ?!, ошибка mypy"}


def problem07() -> dict[int, str]:
    return {25: "Callable ковариантен по значению, а значит передавать можно только подтип B",
            27: "Callable ковариантен по значению, а значит передавать можно только подтип B",
            28: "Callable контрвариантен по аргументам, а значит в аргументах должен идти надтип A"}


def problem08() -> dict[int, str]:
    return {6: "Не все iterable объекты являются sized, mypy ошибка",
            18: "sized, но не iterable, mypy ошибка",
            24: "Iterable, но __iter__ возвращает итератор на int, а надо на str + нет метода __len__"}


def problem09() -> dict[int, str]:
    return {32: "operator in может быть не в любом Fooable",
            34: "[] не имеет метода foo",
            37: "C не соответствует , так как нет __len__",
            38: "Не класс, нет __len__ метода"}


def problem10() -> dict[int, str]:
    return {18: "str не относится к потомкам SupportsFloat протокола, mypy ошибка",
            29: "g принимает A[int] и соответствующие ковариантные потомки, float предок int-a"}

#
# import typing as tp
#
#
# def foo(a: tp.Iterable[str]) -> bool:
#     b = len(a)
#     c = sum(1 for i in a)
#     return b == c
#
#
# foo(["a", "b"])
# foo("ab")
# foo({"a": 2})
#
#
# class A:
#     def __len__(self) -> int:
#         return 1
#
#
# foo(A())
#
#
# class B:
#     def __iter__(self) -> tp.Iterator[int]:
#         return iter([])
#
#
# foo(B())
#
#
# class C:
#     def __iter__(self) -> tp.Iterator[str]:
#         return iter([])
