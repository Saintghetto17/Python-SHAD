import dataclasses
import textwrap

import pytest

from .count_util import count_util


@dataclasses.dataclass
class Case:
    text: str
    flags: str | None
    result: dict[str, int]
    dedent: bool = True

    def __str__(self) -> str:
        return f'[{self.flags}]{self.text[:20]}'

    @property
    def fixed_text(self) -> str:
        if self.dedent:
            return textwrap.dedent(self.text)
        return self.text


TEST_CASES = [
    Case(text='''\
           there is one
             more
         example for
          problem
         ''',
         flags='-m', result={'chars': 45}),
    Case(text='''\
           there is one
             more
         example for
          problem
         ''',
         flags='-l', result={'lines': 4}),
    Case(text='''\
           there is one
             more
         example for
          problem
         ''',
         flags='-L', result={'longest_line': 14}),
    Case(text='''\
           there is one
             more
         example for
          problem
         ''',
         flags='-w', result={'words': 7}),
    Case(text='''\
           there is one
             more
         example for
          problem
         ''',
         flags='-wLlm', result={'chars': 45, 'words': 7, 'lines': 4, 'longest_line': 14}),
    Case(text='''\
           there is one
             more
         example for
          problem
         ''',
         flags='-w -L -l -m', result={'chars': 45, 'words': 7, 'lines': 4, 'longest_line': 14}),
    Case(text='''\
           there is one
             more
         example for
          problem
         ''',
         flags='-w -l', result={'words': 7, 'lines': 4}),
    Case(text='''\
           there is one
             more
         example for
          problem
         ''',
         flags='', result={'chars': 45, 'words': 7, 'lines': 4, 'longest_line': 14}),
    Case(text='''\
           there is one
             more
         example for
          problem
         ''',
         flags=None, result={'chars': 45, 'words': 7, 'lines': 4, 'longest_line': 14}),
    Case(text='''\
         there is
           my secret test
          nobody knows it
         really
         \t
         empty lines
            spaces
                and many words in one string
         ''',
         flags='-wlLm', result={'chars': 109, 'words': 18, 'lines': 8, 'longest_line': 35}),
    Case(text='''\
         and
            very
               simple
                     test
         \n
         ''',
         flags='-l', result={'lines': 6}),
    Case(text='       \n'
              '            \n'
              '     \n',
         flags='-L', result={'longest_line': 12}, dedent=False),
    Case(text='', flags='',
         result={'chars': 0, 'lines': 0, 'words': 0, 'longest_line': 0}),
    Case(text='abc\ndefg', flags='',
         result={'chars': 8, 'lines': 1, 'words': 2, 'longest_line': 4}),
    Case(text='abc\ndefg\n', flags='',
         result={'chars': 9, 'lines': 2, 'words': 2, 'longest_line': 4}),
    Case(text='\n\n\n\n', flags='',
         result={'chars': 4, 'lines': 4, 'words': 0, 'longest_line': 0}),
]


@pytest.mark.parametrize('case', TEST_CASES, ids=str)
def test_count_util(case: Case) -> None:
    answer = count_util(case.fixed_text, case.flags)

    assert answer == case.result
