import io
import math
import sys

import pytest

from .calc import run_calc


def test_basic(capsys, monkeypatch):  # type: ignore
    monkeypatch.setattr(sys, 'stdin', io.StringIO(
        '3 + 5\n'
        '24 / 2\n'
        'math.cos(math.pi)\n'
    ))
    run_calc({'math': math})
    captured = capsys.readouterr()
    assert captured.out == (
        '>>> 8\n'
        '>>> 12.0\n'
        '>>> -1.0\n'
        '>>> \n'
    )


def test_context(capsys, monkeypatch):  # type: ignore
    context = {'foo': lambda x: x * 2}
    monkeypatch.setattr(sys, 'stdin', io.StringIO(
        'foo(2)\n'
        'foo("abc")\n'
        'foo([1, 2, 3])\n'
    ))
    run_calc(context)
    captured = capsys.readouterr()
    assert captured.out == (
        '>>> 4\n'
        '>>> abcabc\n'
        '>>> [1, 2, 3, 1, 2, 3]\n'
        '>>> \n'
    )


def test_context_error(monkeypatch):  # type: ignore
    monkeypatch.setattr(sys, 'stdin', io.StringIO(
        'math.sqrt(144)\n'
        'foo(144)\n'
        'print(123)\n'
    ))
    with pytest.raises(NameError, match='name \'math\' is not defined'):
        run_calc()
    with pytest.raises(NameError, match='name \'foo\' is not defined'):
        run_calc()
    with pytest.raises(NameError, match='name \'print\' is not defined'):
        run_calc()
