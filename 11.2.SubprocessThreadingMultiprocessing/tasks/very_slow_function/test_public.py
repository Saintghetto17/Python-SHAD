import timeit

import testlib

from .very_slow_function import calc_squares_simple, calc_squares_multithreading, calc_squares_multiprocessing


###################
# Structure asserts
###################


def test_used_very_slow_function() -> None:
    assert testlib.is_instruction_used(calc_squares_simple, 'argval', 'very_slow_function')
    assert testlib.is_instruction_used(calc_squares_multithreading, 'argval', 'very_slow_function')
    assert testlib.is_instruction_used(calc_squares_multiprocessing, 'argval', 'very_slow_function')


def test_used_multithreading() -> None:
    assert testlib.is_instruction_used(calc_squares_multithreading, 'argval', 'Thread')


def test_used_multiprocessing() -> None:
    assert testlib.is_instruction_used(calc_squares_multiprocessing, 'argval', 'Pool')


###################
# Tests
###################


def test_correctness() -> None:
    expected_result = [0, 1, 4, 9]
    assert expected_result == calc_squares_simple(4)
    assert expected_result == calc_squares_multithreading(4)
    assert expected_result == calc_squares_multiprocessing(4)


def test_speed() -> None:
    time_simple = timeit.timeit(lambda: calc_squares_simple(50), number=1)
    time_multithreading = timeit.timeit(lambda: calc_squares_multithreading(50), number=1)
    time_multiprocessing = timeit.timeit(lambda: calc_squares_multiprocessing(50), number=1)

    assert time_simple > time_multiprocessing

    print('\nelapsed time for:')
    print(f'\t1. calc_squares_simple: {time_simple:.2f}s')
    print(f'\t2. calc_squares_multithreading: {time_multithreading:.2f}s')
    print(f'\t3. calc_squares_multiprocessing: {time_multiprocessing:.2f}s')
