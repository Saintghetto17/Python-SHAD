import numpy as np
import numpy.typing as npt


def nonzero_product(matrix: npt.NDArray[np.int_]) -> int | None:
    """
    Compute product of nonzero diagonal elements of matrix
    If all diagonal elements are zeros, then return None
    :param matrix: array,
    :return: product value or None
    """
    if not np.any(matrix):
        return None
    diag = np.diag(matrix)
    if not np.any(diag):
        return None
    repl = np.array(diag)
    repl[diag == 0] = 1
    return int(np.prod(repl))
