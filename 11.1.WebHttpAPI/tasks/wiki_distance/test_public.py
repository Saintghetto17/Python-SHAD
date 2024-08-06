import os
from pathlib import Path
from dataclasses import dataclass

import requests
import requests_mock

import pytest
from urllib.parse import quote, unquote

from .wiki_distance import distance


CUR_DIR = Path(__file__).parent


def wiki_url(article: str) -> str:
    return 'https://ru.wikipedia.org/wiki/' + quote(article)


@dataclass
class Case:
    source_article: str
    target_article: str
    distance: int | None

    def __str__(self) -> str:
        return f'{self.source_article} -> {self.target_article}'


CASES = [
    Case(
        source_article='Git',
        target_article='Система_управления_версиями',
        distance=1
    ),
    Case(
        source_article='Предмет',
        target_article='Философия',
        distance=None
    ),
    Case(
        source_article='Гравитация',
        target_article='Римляне',
        distance=2
    ),
    Case(
        source_article='Википедия',
        target_article='Математика',
        distance=10
    ),
    Case(
        source_article='Человек',
        target_article='Цивилизация',
        distance=38
    ),
    Case(
        source_article='Linux',
        target_article='Европа',
        distance=31
    ),
]


def custom_matcher(request: requests_mock.request._RequestObjectProxy) -> requests.Response:
    wiki_page_name = unquote(request.path_url.lstrip('/wiki/'))
    wiki_page_path = os.path.join(CUR_DIR, f'testdata/{wiki_page_name}')
    resp = requests.Response()
    try:
        resp.raw = open(wiki_page_path, 'rb')
        resp.status_code = 200
        resp.encoding = 'utf-8'
    except FileNotFoundError:
        raise requests.exceptions.RequestException
    return resp


@requests_mock.Mocker(kw='m')
@pytest.mark.parametrize('case', CASES, ids=str)
def test_distance(case: Case, **kwargs: requests_mock.Adapter) -> None:
    m = kwargs['m']
    m.add_matcher(custom_matcher)

    assert distance(wiki_url(case.source_article), wiki_url(case.target_article)) == case.distance
