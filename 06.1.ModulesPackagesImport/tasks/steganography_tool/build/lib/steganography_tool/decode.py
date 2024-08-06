import numpy as np
import numpy.typing as npt


def decode_message(data: npt.NDArray[np.ubyte]) -> str:
    width, height = data.shape[0:2]

    data_flatten = np.reshape(data, width * height * 3)

    # extract lsb
    data_flatten = data_flatten & np.ubyte(1)

    # Packs binary-valued array into 8-bits array.
    data_flatten = np.packbits(data_flatten)

    # Read and convert integer to Unicode characters until hitting a non-printable character
    message = []
    for x in data_flatten:
        char = chr(x)
        if not char.isprintable():
            break
        message.append(char)

    return ''.join(message)
