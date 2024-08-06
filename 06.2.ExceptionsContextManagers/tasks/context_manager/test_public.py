import io
from .context_manager import supresser, retyper, dumper


def test_retyper_retypes() -> None:
    try:
        with retyper(ValueError, TypeError):
            raise ValueError('penguin')
    except ValueError:
        assert False, 'source error was raised'
    except TypeError as e:
        assert 'penguin' in e.args, 'attribute args lost'
    except Exception as e:
        assert False, 'totally wrong exception type {}'.format(e)
    else:
        assert False, 'retyper should throw'


def test_retyper_idles() -> None:
    try:
        with retyper(ValueError, TypeError):
            raise IOError
    except (ValueError, TypeError):
        assert False, 'wrong exception type'
    except IOError:
        assert True
    except Exception:
        assert False, 'wrong exception type'
    else:
        assert False, 'retyper should throw'


def test_nested_retypers() -> None:
    try:
        with retyper(TypeError, IOError), retyper(ValueError, TypeError):
            raise ValueError('lalala', 1)
    except IOError as e:
        assert e.args == ('lalala', 1)
    else:
        assert False, 'wrong exception type in nested manager'


def test_supresser_idles() -> None:
    try:
        with supresser(ValueError, TypeError):
            raise IOError
    except IOError:
        assert True
    except Exception as e:
        assert False, 'wrong exception type {}'.format(e)
    else:
        assert False, 'no exception'


def test_supresser_supress() -> None:
    try:
        with supresser(ValueError, TypeError):
            raise ValueError('message')
    except Exception as e:
        assert False, 'supressed exception raised {}'.format(e)
    else:
        pass


def test_dumper_stream() -> None:
    stream = io.StringIO()
    msg = 'message to log'
    try:
        with dumper(stream):
            raise ValueError(msg)
    except ValueError:
        assert msg in stream.getvalue()
    except Exception:
        assert False, 'wrong exception'
    else:
        assert False, 'dumper should throw'


def test_dumped_stderr(capsys) -> None:  # type: ignore
    msg = 'message to log'
    try:
        with dumper():
            raise ValueError(msg)
    except ValueError:
        captured = capsys.readouterr()
        assert msg in captured.err
    except Exception:
        assert False, 'wrong exception'
    else:
        assert False, 'dumper should throw'
