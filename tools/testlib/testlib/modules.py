from pathlib import Path
import sys
import ast


class ImportAnalyzer(ast.NodeVisitor):
    def __init__(self) -> None:
        self.direct_imports: set[str] = set()
        self.from_imports: set[str] = set()

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self.direct_imports.add(alias.name.split(".")[0])

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        # if node.module is missing it's a "from . import ..." statement
        # if level > 0 it's a "from .submodule import ..." statement
        if node.module is not None and node.level == 0:
            self.from_imports.add(node.module.split(".")[0])

    def get_imports(self) -> tuple[set[str], set[str]]:
        print(f'{self.from_imports=}, {self.direct_imports=}')
        return self.from_imports, self.direct_imports


def get_file_imports(filepath: str | Path) -> set[str]:
    filepath = Path(filepath)
    assert filepath.exists() and filepath.is_file()

    with open(filepath) as f:
        tree = ast.parse(f.read())

    analyzer = ImportAnalyzer()
    analyzer.visit(tree)
    from_imports, direct_imports = analyzer.get_imports()

    return {*from_imports, *direct_imports}


def get_module_imports(path: str | Path) -> set[str]:
    path = Path(path)
    assert path.exists()

    if path.is_file():
        return get_file_imports(path)
    else:
        imports: set[str] = set()
        for filepath in path.glob('**/*.py'):
            imports.update(get_file_imports(filepath))
        return imports


def is_module_imported(module_name: str, path: str | Path) -> bool:
    return module_name in get_module_imports(path)


def is_module_imported_hard(module_name: str) -> bool:
    return module_name in sys.modules
