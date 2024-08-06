import numpy as np
import numpy.typing as npt


def nearest_value(matrix: npt.NDArray[np.float_], value: float) -> float | None:
    """
    Find nearest value in matrix.
    If matrix is empty return None
    :param matrix: input matrix
    :param value: value to find
    :return: nearest value in matrix or None
    """
    if len(matrix) == 0 or (len(matrix[0]) == 0 and len(matrix) == 1):
        return None
    mat = abs(matrix - value)
    elem = np.min(mat)
    index = np.argwhere(mat == elem)
    index_x = index[0][0]
    index_y = index[0][1]
    return matrix[index_x][index_y]
