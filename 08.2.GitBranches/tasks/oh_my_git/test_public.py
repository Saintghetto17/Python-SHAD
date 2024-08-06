import importlib
import importlib.util
import os
import shutil
import typing as tp
import zipfile
from hashlib import md5
from pathlib import Path

import git
import pytest

from .oh_my_git import get_secret_code


def _get_parental_set(commit: git.objects.Commit) -> tp.Set[str]:
    return set(commit.hexsha for commit in commit.parents)


def _get_md5ify(inp: str) -> str:
    return md5(inp.encode('ascii')).hexdigest()


def test_get_secret_code() -> None:
    the_code = get_secret_code()
    assert _get_md5ify(the_code) == '6d0c2ab71474079d5a64c2c700706a2d', \
        'The secret code is incorrect, please do try again'


def test_solution_zip_exists() -> None:
    zip_path = Path(__file__).parent / 'repo_solved.zip'
    assert zip_path.exists() and zip_path.is_file()


@pytest.fixture(scope='session')
def repo() -> tp.Generator[git.Repo, None, None]:
    unarchived_path = 'solved'
    zip_path = Path(__file__).parent / 'repo_solved.zip'
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(unarchived_path)
    repo = git.Repo(Path(unarchived_path) / 'repo')
    yield repo
    shutil.rmtree(unarchived_path)


def test_fast_forward(repo: git.Repo) -> None:
    correct_hash = 'e46a669b56981066097567e8cb445f549fd53c9f'
    assert repo.commit('fast_forward_recepient').hexsha == correct_hash, \
        'The recepient in fast forward is not in a correct position'
    assert repo.commit('fast_forward_sender').hexsha == correct_hash, \
        'The sender should never be changed (fast forward)'


def test_automerge(repo: git.Repo) -> None:
    assert _get_parental_set(repo.commit('automerge_recepient')) == {'e46a669b56981066097567e8cb445f549fd53c9f',
                                                                     '63dab292334bc1a06b7614ed596ad9d83aee2191'}, \
        'Automerge recepient does not have the correct parents'
    assert repo.commit('automerge_sender').hexsha == '63dab292334bc1a06b7614ed596ad9d83aee2191', \
        'Sender should not be changed (automerge)'


@tp.no_type_check
def test_conflict_resolution(repo: git.Repo) -> None:
    assert _get_parental_set(repo.commit('conflict_recepient')) == {'e46a669b56981066097567e8cb445f549fd53c9f',
                                                                    'c2be00c557ae7bd1da8a088585d8920cd0a71396'}, \
        'Conflict recepient does not have the correct parents'

    assert repo.commit('conflict_sender').hexsha == 'c2be00c557ae7bd1da8a088585d8920cd0a71396', \
        'Sender should not be changed (conflict)'
    repo.head.reference = repo.heads.conflict_recepient.commit
    repo.head.reset(index=True, working_tree=True)
    pt = os.path.abspath(str(Path(repo.git_dir) / '..' / 'hello_world.py'))

    spec = importlib.util.spec_from_file_location('hello_world', pt)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.get_hello_world() == 'Hello, World!', 'get_hello_world should return the string "Hello, World!"'


def test_move(repo: git.Repo) -> None:
    assert _get_md5ify(repo.commit('move_me_back').hexsha) == '99e902d43b155ee357fb1277a83472cf', \
        'The move_me_back branch should point to the commit where the secret code has been found, but it doesn\'t'
