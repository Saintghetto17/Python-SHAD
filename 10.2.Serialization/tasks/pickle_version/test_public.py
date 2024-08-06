import dataclasses

import pytest

from .pickle_version import get_pickle_version, PickleVersion


@dataclasses.dataclass
class Case:
    name: str
    data: bytes
    expected: PickleVersion

    def __str__(self) -> str:
        return 'test_{}'.format(self.name)


TEST_CASES = [
    Case(
        name='test_protocol_0',
        data=b'(dp0\nVhello\np1\nVshad\np2\nsVsome_key\np3\n(lp4\nI1\naF0.11\nas.',
        expected=PickleVersion(False, -1)
    ),
    Case(
        name='test_protocol_1',
        data=b'}q\x00(X\x05\x00\x00\x00helloq\x01X\x04\x00\x00\x00shadq'
             b'\x02X\x08\x00\x00\x00some_keyq\x03]q\x04(K\x01G?\xbc(\xf5\xc2\x8f\\)eu.',
        expected=PickleVersion(False, -1)
    ),
    Case(
        name='test_protocol_2',
        data=b'\x80\x02]q\x00(K\x01X\x05\x00\x00\x00helloq\x01X\x04\x00\x00\x00shadq'
             b'\x02X\x08\x00\x00\x00some_keyq\x03e.',
        expected=PickleVersion(True, 2)
    ),
    Case(
        name='test_protocol_3',
        data=b'\x80\x03cbuiltins\nset\nq\x00]q\x01(X\x05\x00\x00\x00helloq\x02X\x08\x00\x00\x00'
             b'some_keyq\x03X\x04\x00\x00\x00shadq\x04K\x01e\x85q\x05Rq\x06.',
        expected=PickleVersion(True, 3)
    ),
    Case(
        name='test_protocol_4',
        data=b'\x80\x04\x95!\x00\x00\x00\x00\x00\x00\x00]\x94(C\n0xDEADBEAF\x94\x8c\x04'
             b'shad\x94\x8c\x05hello\x94e.',
        expected=PickleVersion(True, 4)
    ),
    Case(
        name='test_protocol_5',
        data=b'\x80\x05\x95.\x00\x00\x00\x00\x00\x00\x00}\x94(\x8c\x05hello\x94\x8c\x04shad'
             b'\x94\x8c\x08some_key\x94]\x94(K\x01G?\xbc(\xf5\xc2\x8f\\)eu.',
        expected=PickleVersion(True, 5)
    ),
]


@pytest.mark.parametrize('test_case', TEST_CASES, ids=str)
def test_get_fizz_buzz(test_case: Case) -> None:
    result = get_pickle_version(test_case.data)
    assert result == test_case.expected
