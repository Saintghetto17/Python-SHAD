import dis
import json
import types
import typing as tp
from collections import Counter, defaultdict

# Operations grouped by complexity levels

OPERATION_LEVELS = {
    "ASYNC_GEN_WRAP": 4,
    "BEFORE_ASYNC_WITH": 4,
    "BEFORE_WITH": 3,
    "BINARY_OP": 1,
    "BINARY_SUBSCR": 1,
    "BUILD_CONST_KEY_MAP": 2,
    "BUILD_LIST": 2,
    "BUILD_MAP": 2,
    "BUILD_SET": 2,
    "BUILD_SLICE": 2,
    "BUILD_STRING": 2,
    "BUILD_TUPLE": 2,
    "CALL_FUNCTION_EX": 2,
    "CALL": 1,
    "CHECK_EG_MATCH": 2,
    "CHECK_EXC_MATCH": 2,
    "COMPARE_OP": 1,
    "CONTAINS_OP": 1,
    "COPY_FREE_VARS": 3,
    "COPY": 1,
    "DELETE_ATTR": 1,
    "DELETE_DEREF": 3,
    "DELETE_FAST": 1,
    "DELETE_GLOBAL": 1,
    "DELETE_NAME": 1,
    "DELETE_SUBSCR": 1,
    "DICT_MERGE": 2,
    "DICT_UPDATE": 2,
    "END_ASYNC_FOR": 4,
    "EXTENDED_ARG": 1,
    "FOR_ITER": 1,
    "FORMAT_VALUE": 3,
    "GET_AITER": 4,
    "GET_ANEXT": 4,
    "GET_AWAITABLE": 4,
    "GET_ITER": 1,
    "GET_LEN": 1,
    "GET_YIELD_FROM_ITER": 4,
    "IMPORT_FROM": 2,
    "IMPORT_NAME": 2,
    "IMPORT_STAR": 2,
    "IS_OP": 1,
    "JUMP_BACKWARD_NO_INTERRUPT": 1,
    "JUMP_BACKWARD": 1,
    "JUMP_FORWARD": 1,
    "JUMP_IF_FALSE_OR_POP": 1,
    "JUMP_IF_TRUE_OR_POP": 1,
    "KW_NAMES": 2,
    "LIST_APPEND": 2,
    "LIST_EXTEND": 2,
    "LIST_TO_TUPLE": 2,
    "LOAD_ASSERTION_ERROR": 1,
    "LOAD_ATTR": 2,
    "LOAD_BUILD_CLASS": 3,
    "LOAD_CLASSDEREF": 3,
    "LOAD_CLOSURE": 3,
    "LOAD_CONST": 1,
    "LOAD_DEREF": 3,
    "LOAD_FAST": 1,
    "LOAD_GLOBAL": 1,
    "LOAD_METHOD": 3,
    "LOAD_NAME": 1,
    "MAKE_CELL": 3,
    "MAKE_FUNCTION": 2,
    "MAP_ADD": 2,
    "MATCH_CLASS": 2,
    "MATCH_KEYS": 1,
    "MATCH_MAPPING": 1,
    "MATCH_SEQUENCE": 1,
    "NOP": 1,
    "POP_EXCEPT": 1,
    "POP_JUMP_BACKWARD_IF_FALSE": 1,
    "POP_JUMP_BACKWARD_IF_NONE": 1,
    "POP_JUMP_BACKWARD_IF_NOT_NONE": 1,
    "POP_JUMP_BACKWARD_IF_TRUE": 1,
    "POP_JUMP_FORWARD_IF_FALSE": 1,
    "POP_JUMP_FORWARD_IF_NONE": 1,
    "POP_JUMP_FORWARD_IF_NOT_NONE": 1,
    "POP_JUMP_FORWARD_IF_TRUE": 1,
    "POP_TOP": 1,
    "PRECALL": 1,
    "PREP_RERAISE_STAR": 2,
    "PUSH_EXC_INFO": 2,
    "PUSH_NULL": 1,
    "RAISE_VARARGS": 1,
    "RERAISE": 1,
    "RESUME": 1,
    "RETURN_GENERATOR": 4,
    "RETURN_VALUE": 1,
    "SEND": 4,
    "SET_ADD": 2,
    "SET_UPDATE": 2,
    "SETUP_ANNOTATIONS": 3,
    "STORE_ATTR": 1,
    "STORE_DEREF": 3,
    "STORE_FAST": 1,
    "STORE_GLOBAL": 1,
    "STORE_NAME": 1,
    "STORE_SUBSCR": 1,
    "SWAP": 1,
    "UNARY_INVERT": 1,
    "UNARY_NEGATIVE": 1,
    "UNARY_NOT": 1,
    "UNARY_POSITIVE": 1,
    "UNPACK_EX": 2,
    "UNPACK_SEQUENCE": 2,
    "WITH_EXCEPT_START": 3,
    "YIELD_VALUE": 4
}

# Scores for fully covered level

LEVEL_SCORES = {
    0: 0,
    1: 200,
    2: 150,
    3: 50,
    4: 50
}

FULL_SCORE = 400


def generate_stub_operations() -> None:
    """
    Utility function for generation stub for OPERATION_LEVELS
    """
    print(json.dumps({key: 0 for key in dis.opmap}, sort_keys=True, indent=4))


class StatData:
    def __init__(self, code: str, operations: dict[str, int]):
        self.code = code
        self.operations = operations


class Scorer:
    def __init__(
            self,
            tests: list[str],
            level_scores: dict[int, int] = LEVEL_SCORES,
            operations_levels: dict[str, int] = OPERATION_LEVELS,
    ):
        self._level_scores = level_scores
        self._operations_levels = operations_levels
        self._stat = [self._collect(test) for test in tests]

    def _collect(self, text_code: str) -> StatData:
        operations = self.get_operations(text_code)
        return StatData(text_code, operations)

    def get_level_operations_count(self) -> tp.Counter[int]:
        return Counter(self._operations_levels.values())

    def get_operations_count(self) -> int:
        return len(self._operations_levels)

    def get_total_stats(self) -> dict[str, int]:
        total_stat = {key: 0 for key in self._operations_levels}

        for stat in self._stat:
            for key, value in stat.operations.items():
                total_stat[key] += value

        return total_stat

    def get_levels_stats(self) -> dict[int, int]:
        level_stats = {level: 0 for level in self._level_scores}

        for stat in self._stat:
            level = self.get_test_level(stat.operations)
            level_stats[level] += 1

        return level_stats

    def get_levels_coverage(self) -> dict[int, int]:
        total_stats = self.get_total_stats()
        level_stats = {level: 0 for level in self._level_scores}

        for operation, level in self._operations_levels.items():
            if total_stats[operation] > 0:
                level_stats[level] += 1
        return level_stats

    def get_operations_coverage(self) -> int:
        return sum(int(operations_count > 0) for operations_count in self.get_total_stats().values())

    def get_test_level(self, operations: dict[str, int]) -> int:
        level = 1

        for key, value in operations.items():
            level = max(level, self._operations_levels[key])

        return level

    def _extract_operations(self, code_obj: types.CodeType) -> dict[str, int]:
        operations: tp.DefaultDict[str, int] = defaultdict(int)

        for i in dis.get_instructions(code_obj):
            operations[i.opname] += 1

        for const in code_obj.co_consts:
            if isinstance(const, types.CodeType):
                for op, value in self._extract_operations(const).items():
                    operations[op] += value

        return operations

    def get_operations(self, text_code: str) -> dict[str, int]:
        code = compile(text_code, '<stdin>', 'exec')
        return self._extract_operations(code)

    def score(self, text_code: str) -> float:
        """
        Normalize test score by number of tests on the same level
        :param text_code: text code to identify personal score
        :return: score for text code
        """
        operations = self.get_operations(text_code)
        total_stats = self.get_levels_stats()

        level = self.get_test_level(operations)
        return self._level_scores[level] / total_stats[level]

    def total_score(self) -> float:
        return sum(self.score(stat.code) for stat in self._stat)


def dump_tests_stat(stream: tp.TextIO, scorer: Scorer) -> None:
    """
    Utility function for dumping stats about operations coverage
    :param stream: stream to write results
    :param scorer: scorer instance with all tests accumulated in
    """
    data = [
        "\nTest operations distribution:",
        "\n".join("\t{}: {}".format(operation, count)
                  for operation, count in sorted(scorer.get_total_stats().items())),
        "Tests levels distribution:",
        "\n".join("\t{}: {}".format(level, count)
                  for level, count in scorer.get_levels_stats().items()),
        "Operations coverage:",
        "\t" + "{}/{}".format(
            scorer.get_operations_coverage(),
            scorer.get_operations_count()),
        "Operations by levels coverage:",
        "\n".join("\t{}: {}/{}".format(level, count, scorer.get_level_operations_count()[level])
                  for level, count in scorer.get_levels_coverage().items()),
        "Maximum score on tests set:",
        "\t" + str(scorer.total_score()),
        "\n"
    ]
    stream.write("\n".join(data))


if __name__ == "__main__":
    generate_stub_operations()
