from .list_twist import ListTwist


def test_used_only_getattr_setattr() -> None:
    class_methods_and_properties = ListTwist.__dict__.keys()

    assert 'reversed' not in class_methods_and_properties
    assert 'R' not in class_methods_and_properties
    assert 'first' not in class_methods_and_properties
    assert 'F' not in class_methods_and_properties
    assert 'last' not in class_methods_and_properties
    assert 'L' not in class_methods_and_properties
    assert 'size' not in class_methods_and_properties
    assert 'S' not in class_methods_and_properties


def test_default_constructor() -> None:
    extended_list = ListTwist()

    assert extended_list.data == []

    assert extended_list.reversed == []
    assert extended_list.R == []

    assert len(extended_list) == 0
    assert extended_list.size == 0
    assert extended_list.S == 0


def test_constructor_with_parameter() -> None:
    extended_list = ListTwist([1, 2, 3])

    assert extended_list.data == [1, 2, 3]
    assert extended_list == [1, 2, 3]

    assert extended_list.reversed == [3, 2, 1]
    assert extended_list.R == [3, 2, 1]

    assert extended_list[0] == 1
    assert extended_list.first == 1
    assert extended_list.F == 1

    assert extended_list[-1] == 3
    assert extended_list.last == 3
    assert extended_list.L == 3

    assert len(extended_list) == 3
    assert extended_list.size == 3
    assert extended_list.S == 3


def test_constructor_with_iterable() -> None:
    extended_list = ListTwist('cba')

    assert extended_list.data == ['c', 'b', 'a']
    assert extended_list == ['c', 'b', 'a']

    assert extended_list.reversed == ['a', 'b', 'c']
    assert extended_list.R == ['a', 'b', 'c']

    assert extended_list[0] == 'c'
    assert extended_list.first == 'c'
    assert extended_list.F == 'c'

    assert extended_list[-1] == 'a'
    assert extended_list.last == 'a'
    assert extended_list.L == 'a'

    assert len(extended_list) == 3
    assert extended_list.size == 3
    assert extended_list.S == 3


def test_constructor_with_empty_list_parameter() -> None:
    extended_list = ListTwist([])

    assert extended_list.data == []
    assert extended_list == []

    assert extended_list.reversed == []
    assert extended_list.R == []

    assert len(extended_list) == 0
    assert extended_list.size == 0
    assert extended_list.S == 0


def test_list_with_different_objects() -> None:
    extended_list = ListTwist([1, 'a', [3]])

    assert extended_list.data == [1, 'a', [3]]
    assert extended_list == [1, 'a', [3]]

    assert extended_list.reversed == [[3], 'a', 1]
    assert extended_list.R == [[3], 'a', 1]

    assert extended_list[0] == 1
    assert extended_list.first == 1
    assert extended_list.F == 1

    assert extended_list[-1] == [3]
    assert extended_list.last == [3]
    assert extended_list.L == [3]

    assert len(extended_list) == 3
    assert extended_list.size == 3
    assert extended_list.S == 3


def test_after_append() -> None:
    extended_list = ListTwist([1, 'a', [3]])

    extended_list.append((4,))

    assert extended_list.data == [1, 'a', [3], (4,)]
    assert extended_list == [1, 'a', [3], (4,)]

    assert extended_list.reversed == [(4,), [3], 'a', 1]
    assert extended_list.R == [(4,), [3], 'a', 1]

    assert extended_list[0] == 1
    assert extended_list.first == 1
    assert extended_list.F == 1

    assert extended_list[-1] == (4,)
    assert extended_list.last == (4,)
    assert extended_list.L == (4,)

    assert len(extended_list) == 4
    assert extended_list.size == 4
    assert extended_list.S == 4


def test_after_del() -> None:
    extended_list = ListTwist([1, 'a', [3]])

    del extended_list[0]

    assert extended_list.data == ['a', [3]]
    assert extended_list == ['a', [3]]

    assert extended_list.reversed == [[3], 'a']
    assert extended_list.R == [[3], 'a']

    assert extended_list[0] == 'a'
    assert extended_list.first == 'a'
    assert extended_list.F == 'a'

    assert extended_list[-1] == [3]
    assert extended_list.last == [3]
    assert extended_list.L == [3]

    assert len(extended_list) == 2
    assert extended_list.size == 2
    assert extended_list.S == 2


def test_after_pop() -> None:
    extended_list = ListTwist([1, 'a', [3]])

    assert extended_list.pop() == [3]

    assert extended_list.data == [1, 'a']
    assert extended_list == [1, 'a']

    assert extended_list.reversed == ['a', 1]
    assert extended_list.R == ['a', 1]

    assert extended_list[0] == 1
    assert extended_list.first == 1
    assert extended_list.F == 1

    assert extended_list[-1] == 'a'
    assert extended_list.last == 'a'
    assert extended_list.L == 'a'

    assert len(extended_list) == 2
    assert extended_list.size == 2
    assert extended_list.S == 2


def test_after_replace_middle_part_of_list() -> None:
    extended_list = ListTwist([1, 'a', [3]])

    extended_list[1:2] = []

    assert extended_list.data == [1, [3]]
    assert extended_list == [1, [3]]

    assert extended_list.reversed == [[3], 1]
    assert extended_list.R == [[3], 1]

    assert extended_list[0] == 1
    assert extended_list.first == 1
    assert extended_list.F == 1

    assert extended_list[-1] == [3]
    assert extended_list.last == [3]
    assert extended_list.L == [3]

    assert len(extended_list) == 2
    assert extended_list.size == 2
    assert extended_list.S == 2


def test_after_replace_first_part_of_list() -> None:
    extended_list = ListTwist([1, 'a', [3]])

    extended_list[0:2] = []

    assert extended_list.data == [[3]]
    assert extended_list == [[3]]

    assert extended_list.reversed == [[3]]
    assert extended_list.R == [[3]]

    assert extended_list[0] == [3]
    assert extended_list.first == [3]
    assert extended_list.F == [3]

    assert extended_list[-1] == [3]
    assert extended_list.last == [3]
    assert extended_list.L == [3]

    assert len(extended_list) == 1
    assert extended_list.size == 1
    assert extended_list.S == 1


def test_after_replace_last_part_of_list() -> None:
    extended_list = ListTwist([1, 'a', [3]])

    extended_list[1:3] = []

    assert extended_list.data == [1]
    assert extended_list == [1]

    assert extended_list.reversed == [1]
    assert extended_list.R == [1]

    assert extended_list[0] == 1
    assert extended_list.first == 1
    assert extended_list.F == 1

    assert extended_list[-1] == 1
    assert extended_list.last == 1
    assert extended_list.L == 1

    assert len(extended_list) == 1
    assert extended_list.size == 1
    assert extended_list.S == 1


def test_after_replace_all_list() -> None:
    extended_list = ListTwist([1, 'a', [3]])

    extended_list[0:3] = []

    assert extended_list.data == []
    assert extended_list == []

    assert extended_list.reversed == []
    assert extended_list.R == []

    assert len(extended_list) == 0
    assert extended_list.size == 0
    assert extended_list.S == 0


def test_first_after_extend() -> None:
    extended_list = ListTwist([2])

    extended_list += [4, 5]

    assert extended_list.data == [2, 4, 5]
    assert extended_list == [2, 4, 5]

    assert extended_list.reversed == [5, 4, 2]
    assert extended_list.R == [5, 4, 2]

    assert extended_list[0] == 2
    assert extended_list.first == 2
    assert extended_list.F == 2

    assert extended_list[-1] == 5
    assert extended_list.last == 5
    assert extended_list.L == 5

    assert len(extended_list) == 3
    assert extended_list.size == 3
    assert extended_list.S == 3


def test_first_after_extend_by_method() -> None:
    extended_list = ListTwist([2])

    extended_list.extend([4, 5])

    assert extended_list.data == [2, 4, 5]
    assert extended_list == [2, 4, 5]

    assert extended_list.reversed == [5, 4, 2]
    assert extended_list.R == [5, 4, 2]

    assert extended_list[0] == 2
    assert extended_list.first == 2
    assert extended_list.F == 2

    assert extended_list[-1] == 5
    assert extended_list.last == 5
    assert extended_list.L == 5

    assert len(extended_list) == 3
    assert extended_list.size == 3
    assert extended_list.S == 3


def test_first_after_insert_at_front() -> None:
    extended_list = ListTwist([1, 'a', [3]])

    extended_list.insert(0, -1)

    assert extended_list.data == [-1, 1, 'a', [3]]
    assert extended_list == [-1, 1, 'a', [3]]

    assert extended_list.reversed == [[3], 'a', 1, -1]
    assert extended_list.R == [[3], 'a', 1, -1]

    assert extended_list[0] == -1
    assert extended_list.first == -1
    assert extended_list.F == -1

    assert extended_list[-1] == [3]
    assert extended_list.last == [3]
    assert extended_list.L == [3]

    assert len(extended_list) == 4
    assert extended_list.size == 4
    assert extended_list.S == 4


def test_first_after_insert_at_back() -> None:
    extended_list = ListTwist([1, 'a', [3]])

    extended_list.insert(-1, -1)

    assert extended_list.data == [1, 'a', -1, [3]]
    assert extended_list == [1, 'a', -1, [3]]

    assert extended_list.reversed == [[3], -1, 'a', 1]
    assert extended_list.R == [[3], -1, 'a', 1]

    assert extended_list[0] == 1
    assert extended_list.first == 1
    assert extended_list.F == 1

    assert extended_list[-1] == [3]
    assert extended_list.last == [3]
    assert extended_list.L == [3]

    assert len(extended_list) == 4
    assert extended_list.size == 4
    assert extended_list.S == 4


def test_first_after_sort() -> None:
    extended_list = ListTwist([6, 4, 5])

    extended_list.sort()

    assert extended_list.data == [4, 5, 6]
    assert extended_list == [4, 5, 6]

    assert extended_list.reversed == [6, 5, 4]
    assert extended_list.R == [6, 5, 4]

    assert extended_list[0] == 4
    assert extended_list.first == 4
    assert extended_list.F == 4

    assert extended_list[-1] == 6
    assert extended_list.last == 6
    assert extended_list.L == 6

    assert len(extended_list) == 3
    assert extended_list.size == 3
    assert extended_list.S == 3


def test_first_after_clear() -> None:
    extended_list = ListTwist([1, 'a', [3]])
    extended_list.clear()

    assert extended_list.data == []
    assert extended_list == []

    assert extended_list.reversed == []
    assert extended_list.R == []

    assert len(extended_list) == 0
    assert extended_list.size == 0
    assert extended_list.S == 0


def test_first_after_reverse() -> None:
    extended_list = ListTwist([6, 4, 5])

    extended_list.reverse()

    assert extended_list.data == [5, 4, 6]
    assert extended_list == [5, 4, 6]

    assert extended_list.reversed == [6, 4, 5]
    assert extended_list.R == [6, 4, 5]

    assert extended_list[0] == 5
    assert extended_list.first == 5
    assert extended_list.F == 5

    assert extended_list[-1] == 6
    assert extended_list.last == 6
    assert extended_list.L == 6

    assert len(extended_list) == 3
    assert extended_list.size == 3
    assert extended_list.S == 3


def test_after_set_first() -> None:
    extended_list = ListTwist([6, 4, 5])

    extended_list.first = 8

    assert extended_list.data == [8, 4, 5]
    assert extended_list == [8, 4, 5]

    assert extended_list.reversed == [5, 4, 8]
    assert extended_list.R == [5, 4, 8]

    assert extended_list[0] == 8
    assert extended_list.first == 8
    assert extended_list.F == 8

    assert extended_list[-1] == 5
    assert extended_list.last == 5
    assert extended_list.L == 5

    assert len(extended_list) == 3
    assert extended_list.size == 3
    assert extended_list.S == 3


def test_after_set_F() -> None:
    extended_list = ListTwist([6, 4, 5])

    extended_list.F = 8

    assert extended_list.data == [8, 4, 5]
    assert extended_list == [8, 4, 5]

    assert extended_list.reversed == [5, 4, 8]
    assert extended_list.R == [5, 4, 8]

    assert extended_list[0] == 8
    assert extended_list.first == 8
    assert extended_list.F == 8

    assert extended_list[-1] == 5
    assert extended_list.last == 5
    assert extended_list.L == 5

    assert len(extended_list) == 3
    assert extended_list.size == 3
    assert extended_list.S == 3


def test_after_set_last() -> None:
    extended_list = ListTwist([6, 4, 5])

    extended_list.last = 8

    assert extended_list.data == [6, 4, 8]
    assert extended_list == [6, 4, 8]

    assert extended_list.reversed == [8, 4, 6]
    assert extended_list.R == [8, 4, 6]

    assert extended_list[0] == 6
    assert extended_list.first == 6
    assert extended_list.F == 6

    assert extended_list[-1] == 8
    assert extended_list.last == 8
    assert extended_list.L == 8

    assert len(extended_list) == 3
    assert extended_list.size == 3
    assert extended_list.S == 3


def test_after_set_L() -> None:
    extended_list = ListTwist([6, 4, 5])

    extended_list.L = 8

    assert extended_list.data == [6, 4, 8]
    assert extended_list == [6, 4, 8]

    assert extended_list.reversed == [8, 4, 6]
    assert extended_list.R == [8, 4, 6]

    assert extended_list[0] == 6
    assert extended_list.first == 6
    assert extended_list.F == 6

    assert extended_list[-1] == 8
    assert extended_list.last == 8
    assert extended_list.L == 8

    assert len(extended_list) == 3
    assert extended_list.size == 3
    assert extended_list.S == 3


def test_after_set_the_same_size() -> None:
    extended_list = ListTwist([6, 4, 5])

    extended_list.size = 3

    assert extended_list.data == [6, 4, 5]
    assert extended_list == [6, 4, 5]

    assert extended_list.reversed == [5, 4, 6]
    assert extended_list.R == [5, 4, 6]

    assert extended_list[0] == 6
    assert extended_list.first == 6
    assert extended_list.F == 6

    assert extended_list[-1] == 5
    assert extended_list.last == 5
    assert extended_list.L == 5

    assert len(extended_list) == 3
    assert extended_list.size == 3
    assert extended_list.S == 3


def test_after_set_greater_size() -> None:
    extended_list = ListTwist([6, 4, 5])

    extended_list.size = 5

    assert extended_list.data == [6, 4, 5, None, None]
    assert extended_list == [6, 4, 5, None, None]

    assert extended_list.reversed == [None, None, 5, 4, 6]
    assert extended_list.R == [None, None, 5, 4, 6]

    assert extended_list[0] == 6
    assert extended_list.first == 6
    assert extended_list.F == 6

    assert extended_list[-1] is None
    assert extended_list[-2] is None
    assert extended_list.last is None
    assert extended_list.L is None

    assert len(extended_list) == 5
    assert extended_list.size == 5
    assert extended_list.S == 5


def test_after_set_less_size() -> None:
    extended_list = ListTwist([6, 4, 5, 9])

    extended_list.size = 2

    assert extended_list.data == [6, 4]
    assert extended_list == [6, 4]

    assert extended_list.reversed == [4, 6]
    assert extended_list.R == [4, 6]

    assert extended_list[0] == 6
    assert extended_list.first == 6
    assert extended_list.F == 6

    assert extended_list[-1] == 4
    assert extended_list.last == 4
    assert extended_list.L == 4

    assert len(extended_list) == 2
    assert extended_list.size == 2
    assert extended_list.S == 2
