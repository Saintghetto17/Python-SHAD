<<<<<<< HEAD
import os
from pathlib import Path
import subprocess


def get_changed_dirs(git_path: Path, from_commit_hash: str, to_commit_hash: str) -> set[Path]:
    # Переходим в директорию с репозиторием Git
    os.chdir(git_path)
    # Выполняем команду Git для получения списка измененных файлов
    git_command = ["git", "diff", "--name-only", from_commit_hash, to_commit_hash]
    result = subprocess.run(git_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Обрабатываем вывод команды Git
    if result.returncode == 0:
        changed_files = result.stdout.splitlines()
    else:
        raise RuntimeError(f"Git command failed: {result.stderr}")

    # Создаем множество для хранения директорий с измененными файлами
    changed_dirs = set()

    # Проходим по каждому измененному файлу и добавляем его директорию в множество
    for file_path in changed_files:
        # task/task.py
        # full route without task.py
        file_res: Path = Path(str(git_path) + '/' + file_path)
        changed_dirs.add(file_res.parent)
    return changed_dirs
=======
import subprocess
from pathlib import Path


def get_changed_dirs(git_path: Path, from_commit_hash: str, to_commit_hash: str) -> set[Path]:
    """
    Get directories which content was changed between two specified commits
    :param git_path: path to git repo directory
    :param from_commit_hash: hash of commit to do diff from
    :param to_commit_hash: hash of commit to do diff to
    :return: sequence of changed directories between specified commits
    """
>>>>>>> 5b921105b3b183ffd0545c94df6acb72c453398b
