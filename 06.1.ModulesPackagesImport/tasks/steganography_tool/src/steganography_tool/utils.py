from pathlib import Path
import pkg_resources  # type: ignore
from PIL import Image
import numpy as np
import numpy.typing as npt


def read_file(filename: str | Path) -> npt.NDArray[np.ubyte]:
    with Image.open(filename) as img:
        # width, height = img.size
        data = np.array(img, dtype=np.ubyte)

    return data


def write_file(data: npt.NDArray[np.ubyte], filename: str | Path) -> None:
    new_img = Image.fromarray(data)
    new_img.save(filename)


def get_base_file() -> npt.NDArray[np.ubyte]:
    lenna_filename = pkg_resources.resource_filename(__name__, 'lenna.png')
    return read_file(lenna_filename)
