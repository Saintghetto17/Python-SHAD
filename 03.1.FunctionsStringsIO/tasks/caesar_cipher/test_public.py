import dataclasses

import pytest

from .caesar_cipher import caesar_encrypt


@dataclasses.dataclass
class Case:
    message: str
    n: int
    result: str

    def __str__(self) -> str:
        return f'{self.message}__{self.n}'


TEST_CASES = [
    Case(message='This is stupid song stupid stupid stupid song',
         n=10,
         result='Drsc sc cdezsn cyxq cdezsn cdezsn cdezsn cyxq'),
    Case(message='Drsc sc k cdezsn cyxq cdezsn cdezsn cdezsn cyxq',
         n=-10,
         result='This is a stupid song stupid stupid stupid song'),
    Case(message='Help me, im stuck inside this computer',
         n=2,
         result='Jgnr og, ko uvwem kpukfg vjku eqorwvgt'),
    Case(message='Roses are Red, Violets are blue',
         n=4,
         result='Vswiw evi Vih, Zmspixw evi fpyi'),
    Case(message='A', n=1, result='B'),
    Case(message='XYZ', n=5, result='CDE'),
    Case(message='I havent slept for three days, because that would be too long.',
         n=2,
         result='K jcxgpv ungrv hqt vjtgg fcau, dgecwug vjcv yqwnf dg vqq nqpi.'),
    Case(message='AbCdEfGhIjKlMnOp',
         n=-2,
         result='YzAbCdEfGhIjKlMn'),
    Case(message='You can never lose a homing pigeon - '
                 'if your homing pigeon doesn\'t come back, '
                 'what you\'ve lost is a pigeon.',
         n=20,
         result='Sio wuh hypyl fimy u bigcha jcayih - '
                'cz siol bigcha jcayih xiymh\'n wigy vuwe, '
                'qbun sio\'py fimn cm u jcayih.'),
    Case(message='This is stupid song stupid stupid stupid song',
         n=1000,
         result='Ftue ue efgbup eazs efgbup efgbup efgbup eazs'),
    Case(message='Veni vidi vici',
         n=0,
         result='Veni vidi vici'),
    Case(message='Veni vidi vici',
         n=26,
         result='Veni vidi vici'),
    Case(message='Veni vidi vici',
         n=-26,
         result='Veni vidi vici'),
    Case(message='Veni vidi vici',
         n=52,
         result='Veni vidi vici'),
    Case(message='Veni vidi vici',
         n=-52,
         result='Veni vidi vici'),
]


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_caesar_cipher(t: Case) -> None:
    assert caesar_encrypt(t.message, t.n) == t.result


def test_round_trip() -> None:
    message = 'This is stupid song stupid stupid stupid song'
    result = caesar_encrypt(caesar_encrypt(message, 10), -10)
    assert message == result
