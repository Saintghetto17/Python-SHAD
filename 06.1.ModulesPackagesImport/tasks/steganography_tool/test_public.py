import importlib
from importlib import metadata
from pathlib import Path


MODULE_NAME = 'steganography_tool'


def test_modules_installed() -> None:
    try:
        import PIL  # noqa: F401
    except ImportError:
        assert False, 'Can not find `PIL`. It is required?'

    try:
        import steganography_tool  # noqa: F401
    except ImportError:
        assert False, 'Can not find `steganography_tool`. It is installed?'


def test_structure() -> None:
    try:
        import steganography_tool
        import steganography_tool.decode
        import steganography_tool.encode
        import steganography_tool.cli
        import steganography_tool.utils  # noqa: F401
    except ImportError as e:
        assert False, f'Please, mind package structure: {e}'


def test_import_module_import() -> None:
    try:
        from steganography_tool import encode_message, decode_message  # noqa: F401
    except ImportError as e:
        assert False, f'Please, mind package structure: {e}'


def test_submodules_wildcard_import() -> None:
    module = importlib.import_module(MODULE_NAME)
    module_dict = module.__dict__

    assert '__all__' in module_dict, 'You should limit `import *` via __all__'
    assert module_dict['__all__'] == ['encode_message', 'decode_message']


def test_setup_style() -> None:
    task_dir = Path(__file__).resolve().parent

    setup_cfg_file = task_dir / 'pyproject.toml'
    assert setup_cfg_file.exists(), 'You should use `pyproject.toml`'

    # check only dummy setup.py exists
    setup_py_file = task_dir / 'setup.py'
    setup_py_n_lines = open(setup_py_file.as_posix()).read().count("\n")
    assert setup_py_n_lines <= 4, 'You should use `pyproject.toml` in favor of `setup.py` ' \
                                  '(only dummy `setup.py` allowed)'
    with open(setup_py_file.as_posix()) as f:
        assert 'setup()' in f.read(), 'Use dummy `setup.py` file'


def test_module_metadata() -> None:
<<<<<<< HEAD
    module_name = 'steganography_tool'
    module_metadata = metadata.metadata(module_name)
=======
    module_metadata = metadata.metadata(MODULE_NAME)

    # Project metadata
>>>>>>> 681d1014c6915e8db1b6f69ef6bc1f774f37b273
    for metadata_field in ['Author-email', 'Summary', 'Version', 'Requires-Python']:
        assert module_metadata[metadata_field] and module_metadata[metadata_field] != 'UNKNOWN', \
            f'You should add {metadata_field} in metadata'

    # Dependencies
    assert 'Pillow' in module_metadata['Requires-Dist'], 'You should add `Pillow` in requirements (not in build-system)'
