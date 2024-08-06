import numpy as np
import numpy.typing as npt


def add_zeros(x: npt.NDArray[np.int_]) -> npt.NDArray[np.int_]:
    """
    Add zeros between values of given array
    :param x: array,
    :return: array with zeros inserted
    """
    if len(x) == 0:
        val: npt.NDArray[np.int_] = np.ndarray(())
        return val
    last_deleted = np.delete(x, -1)
    zero = np.zeros((len(x) - 1,), dtype=int)
    arr = np.array([last_deleted, zero])
    res_prev = np.ravel(arr, order='F')
    res = np.append(res_prev, x[-1])
    return res
