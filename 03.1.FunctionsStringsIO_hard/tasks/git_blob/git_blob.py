import pathlib
import zlib
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class BlobType(Enum):
    """Helper class for holding blob type"""
    COMMIT = b'commit'
    TREE = b'tree'
    DATA = b'blob'

    @classmethod
    def from_bytes(cls, type_: bytes) -> 'BlobType':
        for member in cls:
            if member.value == type_:
                return member
        assert False, f'Unknown type {type_.decode("utf-8")}'


@dataclass
class Blob:
    """Any blob holder"""
    type_: BlobType
    content: bytes


@dataclass
class Commit:
    """Commit blob holder"""
    tree_hash: str
    parents: list[str]
    author: str
    committer: str
    message: str


@dataclass
class Tree:
    """Tree blob holder"""
    children: dict[str, Blob]


def read_blob(path: Path) -> Blob:
    """
    Read blob-file, decompress and parse header
    :param path: path to blob-file
    :return: blob-file type and content
    """
    file = open(path, 'rb')
    cnt = file.read()
    bytes_obj = zlib.decompress(cnt)
    index_start_word = 0
    index_end_word = -1
    index_start_content = -1
    index_end_content = len(bytes_obj)
    flag = True
    for i in range(index_end_content):
        if bytes_obj[i] == 32:
            flag = False
            continue
        if flag:
            index_end_word = i
        if bytes_obj[i] == 0:
            index_start_content = i + 1
            break
    content = bytes_obj[index_start_content:index_end_content]
    type = bytes_obj[index_start_word:index_end_word + 1]
    if type == b'commit':
        return Blob(BlobType.COMMIT, content)
    elif type == b'tree':
        return Blob(BlobType.TREE, content)
    elif type == b'blob':
        return Blob(BlobType.DATA, content)
    return Blob(BlobType.DATA, b'')


def traverse_objects(obj_dir: Path) -> dict[str, Blob]:
    """
    Traverse directory with git objects and load them
    :param obj_dir: path to git "objects" directory
    :return: mapping from hash to blob with every blob found
    """
    res: dict[str, Blob] = {}
    directories = [dir for dir in pathlib.Path(obj_dir).iterdir() if dir.is_dir()]
    for path in directories:
        for snap in pathlib.Path(path).iterdir():
            path_str = str(snap.resolve())
            hash_sha = path_str.replace('/', '')[-40:]
            res[hash_sha] = read_blob(snap)
    return res


def parse_commit(blob: Blob) -> Commit:
    """
    Parse commit blob
    :param blob: blob with commit type
    :return: parsed commit
    """
    content_blob = str(blob.content)
    length_str = len(content_blob)
    index_message = -1
    count_n = 0
    for i in range(length_str):
        if content_blob[length_str - i - 1] == 'n' and content_blob[length_str - i - 2] == '\\':
            if i == 1 or i == 0:
                continue
            count_n = count_n + 1
        if count_n == 1:
            index_message = i
            break
    message = content_blob[-index_message:-1].replace('\\n', '')
    lst_split: list[str] = content_blob.split('\\n')
    parents = []
    length = len(lst_split)
    tree_hash = ''
    author = ''
    committer = ''
    for i in range(length):
        if i == 0:
            tree_hash = lst_split[i][7:]
            continue
        elif i < length - 2:
            if len(lst_split[i]) == 0:
                continue
            else:
                if lst_split[i][0] == 'p':
                    parents.append(lst_split[i][7:])
                    continue
                elif lst_split[i][0] == 'a':
                    author = lst_split[i][7:]
                    continue
                elif lst_split[i][0] == 'c':
                    committer = lst_split[i][10:]
                    continue
    return Commit(tree_hash, parents, author, committer, message)


def parse_tree(blobs: dict[str, Blob], tree_root: Blob, ignore_missing: bool = True) -> Tree:
    """
    Parse tree blob
    :param blobs: all read blobs (by traverse_objects)
    :param tree_root: tree blob to parse
    :param ignore_missing: ignore blobs which were not found in objects directory
    :return: tree contains children blobs (or only part of them found in objects directory)
    NB. Children blobs are not being parsed according to type.
        Also nested tree blobs are not being traversed.
    """
    res_dict: dict[str, Blob] = {}
    lst_tree: list[bytes] = tree_root.content.split(b' ')[1:]
    length = len(lst_tree)
    for i in range(length):
        index_name = -1
        for j in range(len(lst_tree[i])):
            if lst_tree[i][j] == 0:
                index_name = j
                break
        name = lst_tree[i][:index_name].decode()
        hash_sha = lst_tree[i][index_name + 1:].hex()[:40]
        if hash_sha in blobs.keys():
            res_dict[name] = blobs[hash_sha]
    return Tree(res_dict)


def find_initial_commit(blobs: dict[str, Blob]) -> Commit:
    """
    Iterate over blobs and find initial commit (without parents)
    :param blobs: blobs read from objects dir
    :return: initial commit
    """
    for key in blobs.keys():
        if blobs[key].type_ == BlobType.COMMIT:
            commit = parse_commit(blobs[key])
            if not commit.parents:
                return commit
            else:
                continue
        else:
            continue
    return Commit('', [], '', '', '')


def search_file(blobs: dict[str, Blob], tree_root: Blob, filename: str) -> Blob:
    """
    Traverse tree blob (can have nested tree blobs) and find requested file,
    check if file was not found (assertion).
    :param blobs: blobs read from objects dir
    :param tree_root: root blob for traversal
    :param filename: requested file
    :return: requested file blob
    """
    tree = parse_tree(blobs, tree_root)
    children = tree.children
    for e in children.keys():
        if e == filename:
            return Blob(tree.children[e].type_, tree.children[e].content)
        else:
            if tree.children[e].type_ == BlobType.TREE:
                return search_file(blobs, tree.children[e], filename)
            else:
                continue
    return Blob(BlobType.DATA, b'')
