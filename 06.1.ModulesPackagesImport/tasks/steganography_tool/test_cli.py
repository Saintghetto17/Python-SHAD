from pathlib import Path
import uuid
import subprocess

import pytest


def _run(command: list[str]) -> tuple[int, str, str]:
    """
    IMPORTANT: This way should NOT be used for cli test in particular.
    We do it here ONLY 'cause this tests are framework agnostic (you can choose any framework in this task).
    Please, use library recommended approach to test (e.g. `CliRunner` for `click`)
    """
    result = subprocess.run(command, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


class TestCli:
    @pytest.mark.parametrize('command_name', ['', 'decode', 'encode'])
    def test_help(self, command_name: str) -> None:
        if not command_name:
            command = ['steganography-tool', '--help']
        else:
            command = ['steganography-tool', command_name, '--help']

        code, out, err = _run(command)
        assert code == 0, err
        assert len(out) > 0

    @pytest.mark.parametrize('message', ['secret-message', 'other-message-123-$#', 'and even with spaces'])
    def test_encode_decode(self, message: str, tmp_path: Path) -> None:
        filename = tmp_path / f'{uuid.uuid1()}.png'
        code, out, err = _run(['steganography-tool', 'encode', filename.as_posix(), message])
        assert code == 0, err + out

        assert filename.exists()
        code, out, err = _run(['steganography-tool', 'decode', filename.as_posix()])
        assert code == 0, err + out
        assert out.startswith(message)
