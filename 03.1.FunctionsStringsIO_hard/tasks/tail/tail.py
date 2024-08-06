import os
import sys
import typing as tp
from pathlib import Path


def tail(filename: Path, lines_amount: int = 10, output: tp.IO[bytes] | None = None) -> None:
    """
    :param filename: file to read lines from (the file can be very large)
    :param lines_amount: number of lines to read
    :param output: stream to write requested amount of last lines from file
                   (if nothing specified stdout will be used)
    """
    file_2 = open(Path(filename), 'rb')
    chunk = 1024
    file_2.seek(0, os.SEEK_END)
    file_size = file_2.tell()
    if file_size <= chunk:
        chunk = file_size
    byte_arr_2: bytearray = bytearray(chunk)
    file_2.seek(-chunk, os.SEEK_END)
    current_position = file_2.tell() - file_size
    bts_amount = file_2.readinto(byte_arr_2)
    mem_2 = memoryview(byte_arr_2)
    count_n_2 = 0
    curr_pos = 0
    flag = True
    if lines_amount == 0 or bts_amount == 0:
        if output is None:
            return None
        output.write(b'')
        return None
    while count_n_2 != lines_amount:
        for i in range(bts_amount):
            curr_pos = curr_pos + 1
            if mem_2[bts_amount - i - 1].to_bytes() == b'\n':
                if i != 0:
                    count_n_2 = count_n_2 + 1
                if count_n_2 == lines_amount:
                    curr_pos = curr_pos - 1
                    break
        if count_n_2 < lines_amount:
            if current_position - chunk >= -file_size:
                file_2.seek(current_position - chunk, os.SEEK_END)
                bts_amount = file_2.readinto(byte_arr_2)
                current_position = current_position - chunk
                mem_2 = memoryview(byte_arr_2)
            else:
                if flag:
                    byte_arr_2 = bytearray(current_position + file_size)
                    bts_amount = file_2.readinto(byte_arr_2)
                    mem_2 = memoryview(byte_arr_2)
                    current_position = current_position - chunk
                    flag = False
                else:
                    byte_res: bytearray = bytearray(file_size)
                    file_2.seek(0, 0)
                    file_2.readinto(byte_res)
                    if output is None:
                        sys.stdout.buffer.write(bytes(byte_res))
                        return None
                    output.write(bytes(byte_res))
                    return None
        elif count_n_2 == lines_amount:
            if curr_pos == file_size - 1:
                curr_pos = curr_pos + 1
            byte_res_2: bytearray = bytearray(curr_pos)
            file_2.seek(-curr_pos, os.SEEK_END)
            file_2.readinto(byte_res_2)
            if output is None:
                sys.stdout.buffer.write(bytes(byte_res_2))
                return None
            else:
                output.write(bytes(byte_res_2))
                return None
    file_2.close()
