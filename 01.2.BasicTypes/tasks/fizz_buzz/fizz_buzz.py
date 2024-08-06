from typing import Union
from typing import List


def get_fizz_buzz(n: int) -> list[int | str]:
    """
    If value divided by 3 - "Fizz",
       value divided by 5 - "Buzz",
       value divided by 15 - "FizzBuzz",
    else - value.
    :param n: size of sequence
    :return: list of values.
    """
    list_fb: List[Union[int, str]] = []
    for i in range(n):
        if (i + 1) % 3 == 0 and (i + 1) % 5 == 0:
            list_fb.append("FizzBuzz")
        elif (i + 1) % 3 == 0 and (i + 1) % 5 != 0:
            list_fb.append("Fizz")
        elif (i + 1) % 3 != 0 and (i + 1) % 5 == 0:
            list_fb.append("Buzz")
        else:
            list_fb.append(i + 1)
    return list_fb
