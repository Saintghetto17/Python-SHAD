import importlib
from importlib import metadata
from pathlib import Path

import pytest


def test_modules_installed() -> None:
    try:
        import cryptography  # noqa: F401
    except ImportError:
        assert False, 'Can not find `cryptography`. It is required?'

    try:
        import simple_pass_manager  # noqa: F401
    except ImportError:
        assert False, 'Can not find `simple_pass_manager`. It is installed?'


def test_structure() -> None:
    try:
        import simple_pass_manager
        import simple_pass_manager.manager
        import simple_pass_manager.utils
        import simple_pass_manager.utils.encryption
        import simple_pass_manager.utils.generation  # noqa: F401
    except ImportError as e:
        assert False, f'Please, mind package structure: {e}'


def test_import_module_import() -> None:
    try:
        from simple_pass_manager import PasswordManager  # noqa: F401
        from simple_pass_manager.manager import PasswordManager  # noqa: F811,F401
    except ImportError as e:
        assert False, f'Please, mind package structure: {e}'


@pytest.mark.parametrize(
    'module_name,all_list',
    [
        (
                'simple_pass_manager',
                [
                    'PasswordManager'
                ]
        ),
        (
                'simple_pass_manager.utils',
                [
                    'password_encrypt', 'password_decrypt', 'key_encrypt', 'key_decrypt', 'generate_key',
                    'generate_password', 'generate_urlsafe_password',
                ]
        ),
        (
                'simple_pass_manager.utils.encryption',
                [
                    'password_encrypt', 'password_decrypt', 'key_encrypt', 'key_decrypt', 'generate_key',
                ]
        ),
        (
                'simple_pass_manager.utils.generation',
                [
                    'generate_password', 'generate_urlsafe_password',
                ]
        ),
    ],
)
def test_submodules_wildcard_import(module_name: str, all_list: list[str]) -> None:
    module = importlib.import_module(module_name)
    module_dict = module.__dict__

    assert '__all__' in module_dict, 'You should limit `import *` via __all__'
    assert set(module_dict['__all__']) == set(all_list)


def test_setup_style() -> None:
    task_dir = Path(__file__).resolve().parent

    setup_cfg_file = task_dir / 'setup.cfg'
    assert setup_cfg_file.exists(), 'You should use `setup.cfg`'

    setup_py_file = task_dir / 'setup.py'
    setup_py_n_lines = open(setup_py_file.as_posix()).read().count("\n")
    assert setup_py_n_lines <= 4, 'You should not use `setup.py` in favor of `setup.cfg`'


def test_original_file_deleted() -> None:
    task_dir = Path(__file__).resolve().parent

    original_file = task_dir / 'simple_pass_manager.py'
    assert not original_file.exists(), 'You should delete original file and make a module'


def test_module_metadata() -> None:
    module_name = 'simple_pass_manager'
    module_metadata = metadata.metadata(module_name)

    for metadata_field in ['Author', 'Author-email', 'Summary', 'Version']:
        assert module_metadata[metadata_field] and module_metadata[metadata_field] != 'UNKNOWN', \
            f'You should add {metadata_field} in metadata'
