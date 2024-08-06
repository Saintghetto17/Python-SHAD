from pathlib import Path
import uuid

import numpy as np

from steganography_tool import encode_message, decode_message
from steganography_tool.utils import read_file, write_file, get_base_file


class TestFiles:
    def test_write_read_file(self, tmp_path: Path) -> None:
        tmp_file = tmp_path / f'{uuid.uuid1()}.png'
        data_base = get_base_file()

        write_file(data_base, tmp_file)
        assert tmp_file.exists()

        read_data = read_file(tmp_file)
        assert np.all(read_data == data_base)


class TestEncodeDecode:
    def test_encode_diff(self) -> None:
        message = 'some-secret-message'
        data_base = get_base_file()
        data = encode_message(data=data_base, message=message)

        assert np.mean(np.abs(data_base - data)) < 10

    def test_encode_decode(self) -> None:
        message = 'some-secret-message'
        data_base = get_base_file()

        data = encode_message(data=data_base, message=message)

        decoded_message = decode_message(data=data)

        assert decoded_message.startswith(message)
