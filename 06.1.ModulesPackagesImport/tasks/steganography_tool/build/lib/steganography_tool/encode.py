import numpy as np
import numpy.typing as npt


def encode_message(data: npt.NDArray[np.ubyte], message: str) -> npt.NDArray[np.ubyte]:
    width, height = data.shape[0:2]
    # Encode the message in a series of 8-bit values
    b_message = ''.join(['{:08b}'.format(ord(x)) for x in message])
    b_message_list = [int(x) for x in b_message]

    b_message_length = len(b_message)

    # Flatten the pixel arrays
    flatten_data = np.reshape(data, width * height * 3)

    # Overwrite pixel LSB
    flatten_data[:b_message_length] = flatten_data[:b_message_length] & ~1 | b_message_list

    # Reshape back to an image pixel array
    return np.reshape(data, (height, width, 3))
