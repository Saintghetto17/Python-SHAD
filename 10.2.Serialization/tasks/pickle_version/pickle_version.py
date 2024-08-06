import dataclasses


@dataclasses.dataclass
class PickleVersion:
<<<<<<< HEAD
    is_new_format: bool
    version: int
=======
	is_new_format: bool
	version: int
>>>>>>> 5b921105b3b183ffd0545c94df6acb72c453398b


def get_pickle_version(data: bytes) -> PickleVersion:
    """
    Returns used protocol version for serialization.

    :param data: serialized object in pickle format.
    :return: protocol version.
    """
<<<<<<< HEAD
    # if the first byte is not '\x80' -> 0 | 1
    # the second byte in >=2 versions determines protocol version
    if data[0] != 128:
        return PickleVersion(False, -1)
    return PickleVersion(True, data[1])
=======
>>>>>>> 5b921105b3b183ffd0545c94df6acb72c453398b
