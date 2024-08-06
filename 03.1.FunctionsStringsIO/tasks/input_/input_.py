import sys
import typing as tp


def input_(prompt: str | None = None,
           inp: tp.IO[str] | None = None,
           out: tp.IO[str] | None = None) -> str | None:
    """Read a string from `inp` stream. The trailing newline is stripped.

    The `prompt` string, if given, is printed to `out` stream without a
    trailing newline before reading input.

    If the user hits EOF (*nix: Ctrl-D, Windows: Ctrl-Z+Return), return None.

    `inp` and `out` arguments are optional and should default to `sys.stdin`
    and `sys.stdout` respectively.
    """
    if inp is None:
        if out is None:
            if prompt is not None:
                sys.stdout.write(prompt)
                sys.stdout.flush()

            string_1 = sys.stdin.readline()
            str_new_1 = string_1.replace('\n', '')
            if str_new_1 == '':
                return None
            return str_new_1
        else:
            if prompt is not None:
                out.write(prompt)
                out.flush()
            string_2 = sys.stdin.read()
            str_new_2 = string_2.replace('\n', '')
            if str_new_2 == '':
                return None
            return str_new_2
    else:
        if out is None:
            if prompt is not None:
                sys.stdout.write(prompt)
                sys.stdout.flush()
            string_3 = inp.read()
            str_new_3 = string_3.replace('\n', '')
            if str_new_3 == '':
                return None
            return str_new_3
        else:
            if prompt is not None:
                out.write(prompt)
                out.flush()
            string_4 = inp.read()
            str_new_4 = string_4.replace('\n', '')
            if str_new_4 == '':
                return None
            return str_new_4
