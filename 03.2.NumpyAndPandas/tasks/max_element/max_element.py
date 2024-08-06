import numpy as np
import numpy.typing as npt


def max_element(array: npt.NDArray[np.int_]) -> int | None:
    """
    Return max element before zero for input array.
    If appropriate elements are absent, then return None
    :param array: array,
    :return: max element value or None
    """
    zeroes = np.argwhere(array == 0)
    if len(zeroes) == 0 or len(array) == 1:
        return None
    if np.amax(zeroes) >= len(array) - 1:
        zeroes_other = np.delete(zeroes, len(zeroes) - 1)
        if len(zeroes_other) == 0:
            return None
        return np.amax(array[zeroes_other + 1])
    return np.amax(array[zeroes + 1])
