import copy
import dataclasses
import dis
import types
import typing as tp

import pytest
import testlib

from .banner_search_system import build_index, get_banners, normalize, get_words, get_banner_indices_by_query
from collections.abc import Callable


###################
# Structure asserts
###################


def _is_comprehension(instruction: dis.Instruction, comp_name: str) -> bool:
    return isinstance(instruction.argval, types.CodeType) and instruction.argval.co_name == comp_name


def _is_functional_call(instruction: dis.Instruction) -> bool:
    return instruction.opname == 'LOAD_GLOBAL' and instruction.argval in {'map', 'filter'}


def _check_comprehension_structure(func: Callable[..., tp.Any], comprehension_name: str) -> None:
    is_used_comprehension = any(
        _is_comprehension(i, comprehension_name) for i in testlib.functions._get_function_instructions(func)
    )
    assert is_used_comprehension, "You should use comprehension"

    is_used_functional_call = any(_is_functional_call(i) for i in testlib.functions._get_function_instructions(func))
    assert not is_used_functional_call, "You shouldn't use map/filter functions"

    is_used_loop = any(i.opname == 'SETUP_LOOP' for i in testlib.functions._get_function_instructions(func))
    assert not is_used_loop, "You shouldn't use loops"


def test_get_banner_indices_by_query_structure() -> None:
    assert testlib.is_instruction_used(get_banner_indices_by_query, 'argval', 'heapq')
    assert testlib.is_instruction_used(get_banner_indices_by_query, 'argval', 'heappop')
    assert testlib.is_instruction_used(get_banner_indices_by_query, 'argval', 'heappush')


def test_get_words_structure() -> None:
    _check_comprehension_structure(get_words, '<listcomp>')


###################
# Tests
###################


@dataclasses.dataclass
class IndexCase:
    banners: list[str]
    result: dict[str, list[int]]


INDEX_TEST_CASE = [
    IndexCase(banners=["Стиральный машина - Более 1000 модель!"], result={
        "модель": [0],
        "более": [0],
        "стиральный": [0],
        "машина": [0],
    }),
    IndexCase(banners=["Стильный джинсы со скидка - Скидка 15% от 2999 р"], result={
        'стильный': [0],
        "джинсы": [0],
        "скидка": [0]
    }),
    IndexCase(banners=[
        "Стильный джинсы со скидка - Скидка 15% от 2999 р",
        "Ремонт стиральный машина - Скидка -20%",
    ], result={
        'стильный': [0],
        "джинсы": [0],
        "скидка": [0, 1],
        "ремонт": [1],
        "стиральный": [1],
        "машина": [1],
    }),
    IndexCase(banners=[], result={}),
    IndexCase(banners=[
        "Джинсы джинсы джинсы",
        "Джинсы джинсы джинсы",
    ], result={
        "джинсы": [0, 1]
    }),
    IndexCase(banners=[
        "Джинсы холодильник джинсы",
        "Джинсы машинка джинсы",
    ], result={
        "джинсы": [0, 1],
        "холодильник": [0],
        "машинка": [1]
    }),
    IndexCase(banners=[
        "Джинсы холодильник джинсы машинка",
        "холодильник Джинсы машинка джинсы",
    ], result={
        "джинсы": [0, 1],
        "холодильник": [0, 1],
        "машинка": [0, 1]
    }),
    IndexCase(banners=[
        "Джинсы холодильник джинсы машинка",
        "холодильник Джинсы машинка джинсы",
        "машинка Джинсы машинка джинсы",
        "машинка",
    ], result={
        "джинсы": [0, 1, 2],
        "холодильник": [0, 1],
        "машинка": [0, 1, 2, 3]
    }),
]


@pytest.mark.parametrize('t', INDEX_TEST_CASE)
def test_build_index(t: IndexCase) -> None:
    banners_copy = copy.deepcopy(t.banners)
    index = build_index(banners_copy)

    assert t.banners == banners_copy, "You shouldn't change inputs"
    assert t.result == index


@dataclasses.dataclass
class NormalizeCase:
    text: str
    normalized_text: str


NORMALIZE_TEST_CASE = [
    NormalizeCase(text="?#@*&%", normalized_text=""),
    NormalizeCase(text="Холодильник бесплатно!", normalized_text="холодильник бесплатно"),
    NormalizeCase(text="скидка - Скидка 15% от 2999 р", normalized_text="скидка  скидка  от  р"),
    NormalizeCase(text="", normalized_text=""),
    NormalizeCase(text="Джинсы со скидка 600р", normalized_text="джинсы со скидка р")
]


@pytest.mark.parametrize('t', NORMALIZE_TEST_CASE)
def test_normalize(t: NormalizeCase) -> None:
    assert normalize(t.text) == t.normalized_text


@dataclasses.dataclass
class WordsCase:
    query: str
    words: list[str]


GET_WORDS_TEST_CASE = [
    WordsCase(query="", words=[]),
    WordsCase(query="  ", words=[]),
    WordsCase(query="скидка ", words=["скидка"]),
    WordsCase(query="скидка по номинал", words=["скидка", "номинал"]),
    WordsCase(query="скидка  скидка  от  руб    ", words=["скидка", "скидка"]),
    WordsCase(query="скидка  джинсы   и холодильник в подарок  ", words=["скидка", "джинсы", "холодильник", "подарок"])
]


@pytest.mark.parametrize('t', GET_WORDS_TEST_CASE)
def test_get_words(t: WordsCase) -> None:
    assert get_words(t.query) == t.words


@dataclasses.dataclass
class QueryCase:
    query: str
    banners_indices: tp.Sequence[int]


QUERIES_TEST_CASE = [
    QueryCase(query="600р итд", banners_indices=[]),
    QueryCase(query="Купить Москва холодильник", banners_indices=[]),
    QueryCase(query="Купить холодильник владикавказ", banners_indices=[]),
    QueryCase(query="Купить холодильник", banners_indices=[12]),
    QueryCase(query="Холодильник купить холодильник", banners_indices=[12]),
    QueryCase(query="Из москва холодильник", banners_indices=[10, 14, 17]),
    QueryCase(query="Ремонт итд холодильник", banners_indices=[14, 15, 16, 17]),
    QueryCase(query="Джинсы со скидка 600р", banners_indices=[18, 20, 21]),
    QueryCase(query="Ремонт стиральная машина", banners_indices=[5, 6]),
    QueryCase(query="ozon.ru", banners_indices=[12, 19])
]

BANNERS = [
    "Стиральный машина - Более 1000 модель!",
    "Маленькая стиральный машина - Машина недорого!",
    "Стиральная машина более 545 модель / holodilnik.ru",
    "Стиральная машина ведущий бренд - Неделя скидка!",
    "Стиральная машина - Кэшбэк до 20%",
    "Ремонт стиральная машина Выезд - 0 ₽. - Диагностика - 0 ₽.",
    "Ремонт стиральная машина - Скидка -20%",
    "Починка Стиральная Машина - Быстро и Недорого!",
    "Отремонтировать стиральная машина - на дом от 500₽!",
    "Холодильник.Ру - интернет магазин / holodilnik.ru",
    "Холодильник в Москва! - С гарантия 5 лет!",
    "Холодильник на goods.ru - Кэшбэк до 20%",
    "Купить холодильник на OZON.ru - Доставить завтра",
    "Десяток бренд холодильник - Неделя скидка!",
    "Ремонт холодильник! На дом - в Москва, вызов на дом!",
    "Ремонт холодильник? - Приехать прямо сейчас!",
    "Ремонт холодильник - Ремонт холодильник. Гарантия!",
    "Ремонт холодильник - В Москва и МО",
    "Скидка на джинсы - Покупать на Wildberries!",
    "Джинсы Levis / ozon.ru",
    "Стильный джинсы со скидка - Скидка 15% от 2999 р",
    "Джинсы от 600 руб. на Беру - Скидка и акция каждый день"
]

BANNERS_INDEX = build_index(BANNERS)


@pytest.mark.parametrize('t', QUERIES_TEST_CASE)
def test_get_banners(t: QueryCase) -> None:
    assert get_banners(t.query, BANNERS_INDEX, BANNERS) == [BANNERS[i] for i in t.banners_indices]
