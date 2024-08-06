import copy
import math
from typing import Any

PROMPT = '>>> '


def run_calc(context: dict[str, Any] | None = None) -> None:
    """Run interactive calculator session in specified namespace"""
    if context is not None:
        new_context_1: dict[str, Any] = copy.copy(context)
        new_context_1['__builtins__'] = {}
        while True:
            try:
                inp = input(PROMPT)
                print(eval(inp, new_context_1))
            except EOFError:
                print('')
                break
    else:
        new_context_2: dict[str, dict[str, str]] = {'__builtins__': {}}
        while True:
            try:
                inp = input(PROMPT)
                print(eval(inp, new_context_2))
            except EOFError:
                print('')
                break


if __name__ == '__main__':
    context = {'math': math}
    run_calc(context)
