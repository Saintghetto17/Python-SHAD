import numpy as np
import numpy.typing as npt


def replace_nans(matrix: npt.NDArray[np.float_]) -> npt.NDArray[np.float_]:
    """
    Replace all nans in matrix with average of other values.
    If all values are nans, then return zero matrix of the same size.
    :param matrix: matrix,
    :return: replaced matrix
    """
    to_exit = matrix
    if matrix.size != 0:
        # find all indexes where nan
        nans = np.isnan(matrix)
        if np.all(nans):
            # if all nans - return 0 matrix
            to_exit = np.zeros_like(matrix)
        else:
            # count mean_val without nans
            mean_val = np.nanmean(matrix)
            # replace all nans positions with mean_val
            to_exit[nans] = mean_val
    return to_exit
