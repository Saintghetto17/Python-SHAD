import numpy as np
import numpy.typing as npt


def vander(array: npt.NDArray[np.float_ | np.int_]) -> npt.NDArray[np.float_]:
    """
    Create a Vandermod matrix from the given vector.
    :param array: input array,
    :return: vandermonde matrix
    """
    arr = np.array(range(0, len(array)))
    arr = np.vstack((arr,) * len(array))
    transposed = array[:, np.newaxis]
    len_times = np.hstack((transposed,) * len(array))
    return len_times ** arr
