from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import pytest

from .git_blob import (
    BlobType, Blob, Commit,
    read_blob, traverse_objects, parse_commit, parse_tree, find_initial_commit, search_file
)

OBJECTS_DIR = Path(__file__).parent / 'objects'


@dataclass
class ReadBlobCase:
    path: Path
    result: Blob

    def __str__(self) -> str:
        return str(self.path)


READ_BLOB_TEST_CASES = [
    ReadBlobCase(
        path=OBJECTS_DIR / '71' / 'bbce6c337432e3218cf478a2d7d19b9dc82517',
        result=Blob(type_=BlobType.COMMIT,
                    content=b'tree d609e8996a786bbfc7589731c4bdac474a3305f2\n'
                            b'parent 234596c32559c78f3b65568bc864f37bd9abf10f\n'
                            b'author Vadim Mazaev <vadim-mazaev@mail.ru> 1521759481 +0300\n'
                            b'committer Vadim Mazaev <vadim-mazaev@mail.ru> 1521759481 +0300\n'
                            b'\n'
                            b'Added duration manually into artist to see it in inline list\n')
    ),
    ReadBlobCase(
        path=OBJECTS_DIR / '94' / 'afdb645344569c93e43a8e435a435ccbecab00',
        result=Blob(type_=BlobType.DATA,
                    content=b'FROM python:3.6\n\n'
                            b'MAINTAINER Vadim Mazaev <vadim.mazaev@gmail.com>\n\n'
                            b'RUN apt-get update\n'
                            b'RUN apt-get install -y vim\n\n'
                            b'COPY requirements.txt /\n'
                            b'RUN pip install -r requirements.txt\n\n'
                            b'COPY . /src\n\n'
                            b'CMD cd src && python3 main.py\n')
    ),
    ReadBlobCase(
        path=OBJECTS_DIR / '3f' / 'd51de4c32e61a527c05848230262aa2cb1aca9',
        result=Blob(
            type_=BlobType.TREE,
            content=b'100644 .env.default\x00O\xbd\x19<,\x90\n\x91\x96\x9c\x8f7\xa7GgPO\xb9\xba\xc3'
                    b'100644 .gitignore\x00\x13~\xb3\xa0D\xc0_s3\xc0\x0b<\xba\x8b\xe3\xf4\x0f\xb6\x8b\xf4'
                    b'100644 docker-compose.yml\x00\x0e\x19\xb91r\xb1S\x9by\x00\xd6\x97;\xe6\x99\xb1\xf9\x91\xc3E'
                    b'40000 src\x00E\xbc.\xfa\x97\x99\x08\xb0\xaa\xd1"\x06\xb4\xbc117\x1a\xf4\x18')
    )
]


@pytest.mark.parametrize('case', READ_BLOB_TEST_CASES, ids=str)
def test_read_blob(case: ReadBlobCase) -> None:
    answer = read_blob(case.path)

    assert answer == case.result


def test_traverse_objects() -> None:
    blobs = traverse_objects(OBJECTS_DIR)

    assert set(blobs.keys()) == {
        'deab79b42df8ad85efb5fb6ced0a45c5a972b116', '4fbd193c2c900a91969c8f37a74767504fb9bac3',
        '234596c32559c78f3b65568bc864f37bd9abf10f', '94afdb645344569c93e43a8e435a435ccbecab00',
        '870fd8d47017a2040f8b3db9376aeda74081c598', 'f1095848fa0acb5491b39d87b56f9febf296a31f',
        '71bbce6c337432e3218cf478a2d7d19b9dc82517', '13e993c9d3fe094a9a66dc03e0180c8fd8e5e4bd',
        '137eb3a044c05f7333c00b3cba8be3f40fb68bf4', '965d89f8c23d641d3329b4e565b3cd53b53e39fd',
        '9651b07b05c9799f78620710350e62aef35aaccc', '45bc2efa979908b0aad12206b4bc3131371af418',
        '5d018a9100a649daec070200e802dab809fd534c', 'a9eb7354ef5252a77157bd34ba01150065eb8e98',
        '1bd9ee3785043bb23af69523af7a59b43d1fe533', '3fd51de4c32e61a527c05848230262aa2cb1aca9'
    }

    blob_types_counter = Counter(blob.type_ for blob in blobs.values())
    assert dict(blob_types_counter) == {BlobType.COMMIT: 8, BlobType.TREE: 3, BlobType.DATA: 5}


@dataclass
class ParseCommitCase:
    path: Path
    result: Commit

    def __str__(self) -> str:
        return str(self.path)


PARSE_COMMIT_TEST_CASES = [
    ParseCommitCase(
        path=OBJECTS_DIR / '71' / 'bbce6c337432e3218cf478a2d7d19b9dc82517',
        result=Commit(
            tree_hash='d609e8996a786bbfc7589731c4bdac474a3305f2',
            parents=['234596c32559c78f3b65568bc864f37bd9abf10f'],
            author='Vadim Mazaev <vadim-mazaev@mail.ru> 1521759481 +0300',
            committer='Vadim Mazaev <vadim-mazaev@mail.ru> 1521759481 +0300',
            message='Added duration manually into artist to see it in inline list'
        )
    ),
    ParseCommitCase(
        path=OBJECTS_DIR / '13' / 'e993c9d3fe094a9a66dc03e0180c8fd8e5e4bd',
        result=Commit(
            tree_hash='3fd51de4c32e61a527c05848230262aa2cb1aca9',
            parents=[],
            author='Vadim Mazaev <vadim-mazaev@mail.ru> 1521583303 +0300',
            committer='Vadim Mazaev <vadim-mazaev@mail.ru> 1521583303 +0300',
            message='Initial commit'
        )
    ),
    ParseCommitCase(
        path=OBJECTS_DIR / 'a9' / 'eb7354ef5252a77157bd34ba01150065eb8e98',
        result=Commit(
            tree_hash='197dd79dc4624c96e0dd2ab3300568c9ce49779c',
            parents=['13e993c9d3fe094a9a66dc03e0180c8fd8e5e4bd'],
            author='Vadim Mazaev <vadim-mazaev@mail.ru> 1521583411 +0300',
            committer='GitHub <noreply@github.com> 1521583411 +0300',
            message='Create LICENSE'
        )
    )
]


@pytest.mark.parametrize('case', PARSE_COMMIT_TEST_CASES, ids=str)
def test_parse_commit(case: ParseCommitCase) -> None:
    answer = parse_commit(read_blob(case.path))

    assert answer == case.result


@dataclass
class ParseTreeCase:
    path: Path
    result: dict[str, BlobType]

    def __str__(self) -> str:
        return str(self.path)


PARSE_TREE_TEST_CASES = [
    ParseTreeCase(
        path=OBJECTS_DIR / '3f' / 'd51de4c32e61a527c05848230262aa2cb1aca9',
        result={
            '.env.default': BlobType.DATA,
            '.gitignore': BlobType.DATA,
            'src': BlobType.TREE
        }
    ),
    ParseTreeCase(
        path=OBJECTS_DIR / '45' / 'bc2efa979908b0aad12206b4bc3131371af418',
        result={
            'Dockerfile': BlobType.DATA,
            'main.py': BlobType.DATA,
            'requirements.txt': BlobType.DATA
        }
    )
]


@pytest.mark.parametrize('case', PARSE_TREE_TEST_CASES, ids=str)
def test_parse_tree(case: ParseTreeCase) -> None:
    answer = parse_tree(traverse_objects(OBJECTS_DIR), read_blob(case.path), ignore_missing=True)

    assert {k: v.type_ for k, v in answer.children.items()} == case.result


def test_find_initial_commit() -> None:
    answer = find_initial_commit(traverse_objects(OBJECTS_DIR))

    assert answer.parents == []
    assert answer.tree_hash == '3fd51de4c32e61a527c05848230262aa2cb1aca9'


@dataclass
class SearchFileCase:
    tree_blob: Path
    filename: str
    content: bytes

    def __str__(self) -> str:
        return str(self.tree_blob)


SEARCH_FILE_TEST_CASES = [
    SearchFileCase(
        tree_blob=OBJECTS_DIR / '3f' / 'd51de4c32e61a527c05848230262aa2cb1aca9',
        filename='.gitignore',
        content=b'.ipynb_checkpoints\n.idea\n*.py[cod]\nvenv\n__pycache__\n.env\n*.crt\n'
    ),
    SearchFileCase(
        tree_blob=OBJECTS_DIR / '3f' / 'd51de4c32e61a527c05848230262aa2cb1aca9',
        filename='Dockerfile',
        content=b'FROM python:3.6\n\n'
                b'MAINTAINER Vadim Mazaev <vadim.mazaev@gmail.com>\n\n'
                b'RUN apt-get update\n'
                b'RUN apt-get install -y vim\n\n'
                b'COPY requirements.txt /\n'
                b'RUN pip install -r requirements.txt\n\n'
                b'COPY . /src\n\n'
                b'CMD cd src && python3 main.py\n'
    ),
]


@pytest.mark.parametrize('case', SEARCH_FILE_TEST_CASES, ids=str)
def test_search_file(case: SearchFileCase) -> None:
    answer = search_file(traverse_objects(OBJECTS_DIR), read_blob(case.tree_blob), case.filename)

    assert answer.type_ is BlobType.DATA
    assert answer.content == case.content


def test_total() -> None:
    blobs = traverse_objects(OBJECTS_DIR)
    commit = find_initial_commit(blobs)
    commit_tree = blobs[commit.tree_hash]

    file_blob = search_file(blobs, commit_tree, 'requirements.txt')
    file_data = file_blob.content.decode()

    assert 'telegram' in file_data
